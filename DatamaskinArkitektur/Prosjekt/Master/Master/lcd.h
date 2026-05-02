/*
 * lcd.h - LCD 16x2 HD44780, 4-bit modus
 *
 * Kobling:
 *   RS  -> PD0
 *   E   -> PD3
 *   RW  -> GND
 *   D4  -> PB0
 *   D5  -> PB1
 *   D6  -> PB2
 *   D7  -> PB3
 */

#ifndef LCD_H
#define LCD_H

#define F_CPU 1000000UL
#include <avr/io.h>
#include <util/delay.h>
#include <stdint.h>

#define RS PD0
#define E  PD3

static void LCD_enable(void)
{
    PORTD |=  (1 << E);
    _delay_us(10);
    PORTD &= ~(1 << E);
    _delay_us(100);
}

/* Sender 4 bit via PB0-PB3 (= LCD D4-D7) */
static void LCD_write_nibble(uint8_t nibble)
{
    PORTB = (PORTB & 0xF0) | (nibble & 0x0F);
    LCD_enable();
}

void LCD_Command(uint8_t cmd)
{
    PORTD &= ~(1 << RS);          /* RS=0: kommando    */
    LCD_write_nibble(cmd >> 4);    /* Ovre nibble forst */
    LCD_write_nibble(cmd & 0x0F);  /* Nedre nibble      */
    _delay_ms(2);
}

void LCD_Char(unsigned char c)
{
    PORTD |=  (1 << RS);         /* RS=1: data */
    LCD_write_nibble(c >> 4);
    LCD_write_nibble(c & 0x0F);
    _delay_us(200);
}

void LCD_String(char *str)
{
    while (*str)
        LCD_Char(*str++);
}

void LCD_String_xy(uint8_t row, uint8_t col, char *str)
{
    uint8_t addr = (row == 0) ? (0x80 | (col & 0x0F))
                               : (0xC0 | (col & 0x0F));
    LCD_Command(addr);
    LCD_String(str);
}

void LCD_Init(void)
{
    DDRB |=  0x0F;                          /* PB0-PB3 som utgang (data) */
    DDRD |=  (1 << RS) | (1 << E);          /* PD0, PD3 som utgang       */
    PORTB &= ~0x0F;
    PORTD &= ~((1 << RS) | (1 << E));

    _delay_ms(100);                          /* Vent paa power-on         */

    /* Tving 8-bit modus 3 ganger (spesiell oppstartsekvens) */
    PORTD &= ~(1 << RS);                     /* RS=0 */

    PORTB = (PORTB & 0xF0) | 0x03;          /* nibble 0x3 */
    LCD_enable();
    _delay_ms(5);

    PORTB = (PORTB & 0xF0) | 0x03;
    LCD_enable();
    _delay_us(200);

    PORTB = (PORTB & 0xF0) | 0x03;
    LCD_enable();
    _delay_us(200);

    /* Bytt til 4-bit modus */
    PORTB = (PORTB & 0xF0) | 0x02;          /* nibble 0x2 */
    LCD_enable();
    _delay_us(200);

    /* Naa i 4-bit modus - fulle kommandoer */
    LCD_Command(0x28);                       /* 4-bit, 2 linjer, 5x8     */
    LCD_Command(0x0C);                       /* Display on, cursor off   */
    LCD_Command(0x01);                       /* Clear                    */
    _delay_ms(5);
    LCD_Command(0x06);                       /* Entry mode: inkrement    */
}

#endif /* LCD_H */
