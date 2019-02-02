#ifndef MOTION_PLANNER_H
#define MOTION_PLANNER_H
#include "mbed.h"

#define MOTION_PLANNER_TIMER_PERIOD 1       // us (microseconds)
#define MOTION_PLANNER_TIMER_WIDTH 0x100000000    // 2^16 (16-bit timer)

struct limit_t {
    DigitalIn * pin;
    int32_t pos;
    bool invert;
};


class MotionPlanner
{
  public:
    MotionPlanner(TIM_TypeDef * timer,
                  DigitalOut &xs, bool invert_xs,
                  DigitalOut &xd, bool invert_xd);
    static void initTimer(TIM_TypeDef * timer, IRQn_Type irq_type);
    
    void setAcceleration(uint32_t acceleration);
    void setSpeed(uint32_t speed);
    void move(int32_t distance);
    void absoluteMove(int32_t dist);
    void active();
    void wait();
    void prepareMove(int32_t dist);
    void prepareAbsoluteMove(int32_t dist);
    void startMove();
    volatile bool motion_planned;
    volatile bool motion_prepared;
    
    void home();
    void home(uint32_t v);
    void set_limitswitch(DigitalIn &pin, int32_t position, bool invert);
    void set_limitswitch(limit_t limit);
    limit_t limits[2];
    uint8_t limit_count;
    bool get_limitswitch(int i);
    char get_limitswitch_char(int i);
    
    int32_t position;

  private:
    static uint8_t _instance_count;
    static MotionPlanner * _irq_table[4];
    TIM_TypeDef * _tim_ptr;
    volatile uint32_t * _tim_ccr_ptr;
    uint8_t _tim_channel;
    uint32_t _tim_sr_mask;
    uint32_t _tim_en_mask;
    static void _IRQHandler(void);
    
    DigitalOut *_stepio;
    int8_t _invert_stepio;
    DigitalOut *_dirio;
    int8_t _invert_dirio;

    volatile uint8_t _phase;
    volatile uint64_t _tcurrent;
    volatile uint64_t _tdecel;
    volatile uint32_t _tdelta;
    uint32_t _tdelta_init;
    uint64_t _xtarget;
    volatile uint64_t _xcurrent;
    volatile uint64_t _xdecel;
    uint32_t _vtarget;
    volatile uint32_t _vcurrent;
    uint32_t _atarget;
    
    bool _homing;
    
    uint32_t _next_timer_value;

    void _step();
    inline void _stepHigh();
    inline void _stepLow();
    inline void _stopMotion();
    inline void _setTimer();
    inline void _clearTimer();
    inline uint32_t _getTimerValue();
};

#endif // MOTION_PLANNER_H
