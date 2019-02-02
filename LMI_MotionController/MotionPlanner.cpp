#include "mbed.h"
#include "MotionPlanner.h"
#include <math.h>

const uint32_t mp_tim_sr_masks[] = {TIM_SR_CC1IF,   TIM_SR_CC2IF,   TIM_SR_CC3IF,   TIM_SR_CC4IF};
const uint32_t mp_tim_en_masks[] = {TIM_DIER_CC1IE, TIM_DIER_CC2IE, TIM_DIER_CC3IE, TIM_DIER_CC4IE};

uint8_t MotionPlanner::_instance_count = 0;
MotionPlanner * MotionPlanner::_irq_table[4] = {NULL, NULL, NULL, NULL};


MotionPlanner::MotionPlanner(TIM_TypeDef * timer,
                             DigitalOut &xs, bool invert_xs,
                             DigitalOut &xd, bool invert_xd){
    _stepio = &xs;
    _invert_stepio = invert_xs ? 1 : 0;
    _dirio = &xd;
    _invert_dirio = invert_xd ? 1 : 0;
    _tim_ptr = timer;
    
    bool channel_found = false;
    for(_tim_channel=0; _tim_channel<4; _tim_channel++){
        bool channel_free = true;
        for(uint8_t j=0; j<_instance_count; j++){
            if(_irq_table[j]->_tim_ptr == _tim_ptr &&
               _irq_table[j]->_tim_channel == _tim_channel){
                    channel_free = false;
                    break;
            }
        }
        if(channel_free) break;
    }
    if(!channel_found){
//        MBED_ERROR(MBED_MAKE_ERROR(MBED_MODULE_APPLICATION, MBED_ERROR_CODE_OUT_OF_RESOURCES), "No more channel available on this timer" );
        printf("ERROR: No free channels left on specified timer!");
    }
    
    printf("Motion planner using timer channel %d\n", _tim_channel+1);
    switch(_tim_channel){
        case 0:
            _tim_ccr_ptr = &(_tim_ptr->CCR1);
            break;
        case 1:
            _tim_ccr_ptr = &(_tim_ptr->CCR2);
            break;
        case 2:
            _tim_ccr_ptr = &(_tim_ptr->CCR3);
            break;
        case 3:
            _tim_ccr_ptr = &(_tim_ptr->CCR4);
            break;
    }
    _tim_sr_mask = mp_tim_sr_masks[_tim_channel];
    _tim_en_mask = mp_tim_en_masks[_tim_channel];
    
    _irq_table[_instance_count] = this;
    _instance_count++;
    
    position = 0;
    motion_prepared = false;
    motion_planned = false;
    limit_count = 0;
    _homing = false;
}

void MotionPlanner::set_limitswitch(DigitalIn &pin, int32_t position, bool invert){
    limit_t limit = {&pin, position, invert};
    set_limitswitch(limit);
}

void MotionPlanner::set_limitswitch(limit_t limit){
    if(limit_count > 0){
        if(limits[0].pos > limit.pos){
            limits[1] = limits[0];
            limits[0] = limit;
        }else{
            limits[1] = limit;
        }
    }else{
        limits[0] = limit;
    }
    limit_count++;
}

bool MotionPlanner::get_limitswitch(int i){
    if(i >= limit_count) return false;
    return *(limits[i].pin) ^ limits[i].invert;
}

char MotionPlanner::get_limitswitch_char(int i){
    if(i >= limit_count) return ' ';
    return get_limitswitch(i) ? 'X' : '-';
}

void MotionPlanner::home(){
    home(0);
}

void MotionPlanner::home(uint32_t v){
    if(limit_count <= 0) return;
    while(motion_planned || motion_prepared);
    uint32_t vtarget = _vtarget;
    uint32_t atarget = _atarget;
    
    if(v > 0) _vtarget = v;
    else _vtarget /= 2;
    
    _homing = true;
    move(-1);
    while(motion_planned || motion_prepared);
    _homing = false;
    position = 0;
    _vtarget = vtarget;
    _atarget = atarget;
}

void MotionPlanner::_stepHigh(){
    *_stepio = 1 ^ _invert_stepio;
}

void MotionPlanner::_stepLow(){
    *_stepio = 0 ^ _invert_stepio;
}

void MotionPlanner::setAcceleration(uint32_t acceleration){
    _atarget = acceleration;
    _tdelta_init = sqrt(static_cast<double>(2000000000000L/_atarget));                 // sqrt(2*10^12 / a)
}

void MotionPlanner::setSpeed(uint32_t speed){
    _vtarget = speed;
}

void MotionPlanner::initTimer(TIM_TypeDef * timer, IRQn_Type irq_type){
    timer->CR1 = TIM_CR1_URS;       // Enable counter
    timer->EGR = TIM_EGR_UG;
    timer->CR2 = 0;
    timer->SMCR = 0;
    timer->DIER = 0;
    timer->SR = 0;
    timer->EGR = TIM_EGR_UG;
    timer->CCMR1 = 0;
    timer->CCMR2 = 0;
    timer->CCER = 0;
    timer->CNT = 0;
    timer->PSC = 83;                      // Precaler: division - 1
    timer->ARR = 0xFFFFFFFF;
    timer->CCR1 = 0;
    timer->CCR2 = 0;
    timer->CCR3 = 0;
    timer->CCR4 = 0;
    timer->DCR = 0;
    timer->DMAR = 0;
    timer->OR = 0;
    timer->EGR = TIM_EGR_UG;
    timer->CR1 |= TIM_CR1_CEN;       // Enable counter
    NVIC_SetVector(irq_type, (uint32_t)&_IRQHandler);
    NVIC_EnableIRQ(irq_type);
    NVIC_SetPriority(irq_type, 0);
}

uint32_t MotionPlanner::_getTimerValue(){
    return _tim_ptr->CNT;
}

void MotionPlanner::absoluteMove(int32_t dist){
    prepareAbsoluteMove(dist);
    startMove();
}

void MotionPlanner::move(int32_t dist){
    prepareMove(dist);
    startMove();
}

void MotionPlanner::startMove(){
    if(!motion_prepared) return;
    motion_planned = true;
    motion_prepared = false;
    _step();
}

void MotionPlanner::prepareAbsoluteMove(int32_t dist){
    prepareMove(dist - position);
}

void MotionPlanner::prepareMove(int32_t dist){
    if(motion_planned) printf("Waiting for prev motion to finish\n");
    while(motion_planned);                                  // Wait for current motion move to stop
    printf("Moving %d steps\n", dist);
    
    motion_prepared = true;
    _xtarget = abs(dist);
    _phase = 0;
    _tcurrent = 0;
    _xcurrent = 0;
    *_dirio = ((dist >= 0) ? 1 : 0) ^ _invert_dirio;
    
    position += dist;
}

void MotionPlanner::wait(){
    while(motion_planned);
}

void MotionPlanner::_step(){
    if(_homing && get_limitswitch(0)){
        printf("Reached home: %u steps\n", (uint32_t)_xcurrent);        //uint64_t doesn't work..., also not wtih %llu format
        _stopMotion();
        return;
    }
    _stepHigh();
    _xcurrent += 1;
    switch(_phase){
        case 0:
            // Initial step...
            _tdelta = _tdelta_init;
            _next_timer_value = _getTimerValue();
            _phase = 1;
            break;
        case 1:
            // Accelerate to v-target
            _vcurrent = _atarget * _tcurrent / 1000000;           // st/s
            _tdelta = 1000000 / _vcurrent;                        // us
            if(!_homing && _xcurrent >= _xtarget / 2){
                _phase = 3;
                _tdecel = _tcurrent;
            }else if(_vcurrent >= _vtarget){
                _vcurrent = _vtarget;
                _tdelta = 1000000 / _vcurrent;
                _xdecel = _xtarget - _xcurrent;
                _tdecel = _tcurrent;
                _phase = 2;
            }
            break;
        case 2:
            // Constant velocity section, previous v and dt values are still valid
            // So, nothing to calculate here... Only checking when to go to the next phase
            if(!_homing && _xcurrent >= _xdecel) _phase = 3;
            break;
        case 3:
            // Deccelerate to v=0
            _vcurrent = _atarget * _tdecel / 1000000;
            _tdelta = 1000000 / _vcurrent;
            if(_xcurrent >= _xtarget){
                _stopMotion();
                return;
            }
            else if(_tdelta >= _tdecel){
                _phase = 4;
                _tdelta = _tdelta_init;
            }
            _tdecel -= _tdelta;
            break;
        case 4:
            // Steps padding, keep stepping with v-init until the target position is reached
            // End of phase 3 already set the right dt, so again, nothing to do here
            // Only checking whether we have reached our target...
            if(_xcurrent >= _xtarget){
                _stopMotion();
                return;
            }
            break;
    }
    wait_us(2);                     // Delay needed, because the motion planner is too fast for the stepper drivers
                                    // Without this, the step pulse is too short (must be >= 2.2us)
    _tcurrent += _tdelta;
    _setTimer();
    _stepLow();
}

void MotionPlanner::_stopMotion(){
    motion_planned = false;
    _stepLow();
    _clearTimer();
}

void MotionPlanner::_setTimer(){
    _next_timer_value = _next_timer_value + _tdelta;        // Make overflow possible, uint8_t to count the number of overflows
    if(_next_timer_value - _tim_ptr->CNT < 10 || (_next_timer_value < _tim_ptr->CNT && _tim_ptr->CNT > 2^30)){
        _next_timer_value = _tim_ptr->CNT + 10;
    }
    *_tim_ccr_ptr = _next_timer_value;
    _tim_ptr->DIER |= _tim_en_mask;
}

void MotionPlanner::_clearTimer(){
    _tim_ptr->DIER &= ~_tim_en_mask;
}

void MotionPlanner::_IRQHandler (void)
{
    for(uint8_t i=0; i<_instance_count; i++){
        MotionPlanner * mp = _irq_table[i];
        if(mp == NULL) continue;                        // Skip NULL pointers
        if((mp->_tim_ptr->SR) & (mp->_tim_sr_mask)){    // If interrupt flag set
            mp->_step();                                 // Step axis
            mp->_tim_ptr->SR &= ~(mp->_tim_sr_mask);    // Clear interrupt flag
        }
    }
}