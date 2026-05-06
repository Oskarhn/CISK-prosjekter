#ifndef ADC_H
#define ADC_H
 
#include <avr/io.h>
#include <stdint.h>
 
void ADC_Init(void)
{
    ADMUX = (1 << REFS0);
 
    /* ADEN = 1 aktiver ADC                  */
    /* ADPS2:0 = 011 -> prescaler 8 (125kHz) */
    ADCSRA = (1 << ADEN) | (1 << ADPS1) | (1 << ADPS0);
}
 
uint16_t ADC_Read(uint8_t channel)
{
    /* Velg kanal, behold referanseinnstilling */
    ADMUX = (ADMUX & 0xE0) | (channel & 0x1F);
 
    ADCSRA |= (1 << ADSC);              /* Start konvertering */
    while (ADCSRA & (1 << ADSC));       /* Vent pa ferdig     */
 
    return ADC; 
 
#endif