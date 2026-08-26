#ifndef ADC_H
#define ADC_H
 
#include <avr/io.h>
#include <stdint.h>
 
#define IR_THRESHOLD  200
#define IR_CHANNEL      1  /* PA1 = ADC1, MUX4:0 = 00001 */
 
void ADC_Init(void)
{
    /* REFS1:0 = 01 -> AVCC som referanse */
    /* MUX4:0 = 00001 -> ADC1 (PA1)       */
    ADMUX  = (1 << REFS0) | (IR_CHANNEL & 0x1F);
 
    /* ADEN=1, prescaler 8 (ADPS1:ADPS0=1:1) */
    ADCSRA = (1 << ADEN) | (1 << ADPS1) | (1 << ADPS0);
}
 
uint16_t ADC_Read_IR(void)
{
    ADCSRA |= (1 << ADSC);         /* Start konvertering */
    while (ADCSRA & (1 << ADSC));  /* Vent pa ferdig     */
    return ADC;
}
 
uint8_t IR_Detect(void)
{
    return (ADC_Read_IR() > IR_THRESHOLD) ? 1 : 0;
}
 
#endif