#ifndef ADC_H
#define ADC_H
 
#include <avr/io.h>
#include <stdint.h>
 
void ADC_Init(void)
{
    /* REFS1:0 = 01 -> AVCC referanse */
    /* MUX4:0  = 00000 -> ADC0 (PA0) */
    ADMUX  = (1 << REFS0);
 
    /* ADEN=1, prescaler 8 */
    ADCSRA = (1 << ADEN) | (1 << ADPS1) | (1 << ADPS0);
}
 
static uint16_t ADC_Read_Raw(void)
{
    /* Velg ADC0 (kanal 0) */
    ADMUX &= 0xE0;
 
    ADCSRA |= (1 << ADSC);         /* Start */
    while (ADCSRA & (1 << ADSC));  /* Vent  */
    return ADC;
}
 
#endif