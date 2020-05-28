# Ray-Gun for the Sharp X68000 - English Translation

## General Notes

*"Georgie is a young man who lives with his fiancee Miria in the quiet town of Lakeside, repairing large combat robots which are strangely called "steroids". One day he discovers several such steroids in the forest, and as he decides to inspect them, unknown flying steroids kidnap Miria. Now Georgie has to pilot a steroid himself and to rescue his beloved one.*

*Ray Gun is a traditional Japanese RPG, with top-down navigation, random turn-based battles viewed from first-person perspective, etc. The combat is usually between the player's steroids and enemy ones. Steroids can attack normally or execute special techniques. Many cut scenes feature nudity."*

Description from [Mobygames.com](https://www.mobygames.com/game/sharp-x68000/ray-gun)


Ray Gun is a fairly early/simplistic RPG game for the NEC PC-88, MSX and Sharp X68000.

This is my attempt to translate the content of the game to English. Why? Well it's a pretty simple game, the text is (mainly) stored uncompressed and in standard S-JIS form and I thought it would be fun to try something that doesn't appear to be very well known!

## Booting & Secret Menu

The game starts from Disk A / Disk 1, which you should have in the first drive, you also need Disk B / Disk 2 in the second drive.

There is a hidden menu with some secret content; if you swap Disk 1 and Disk 2 (i.e. you have Disk 2 in the first drive and Disk 1 in the second drive on boot) you instead get a bonus content of a secret menu.

The bonus menu offers the following content:

- A slideshow of the various *not-safe-for-work* animations without having to unlock them
- A music test mode

## Text Format

Unless otherwise noted, all text is in Shift-JIS format and represented by two bytes within the game files.

## Translation Caveats

I am not a Japanese speaker, neither can I read Hiragana, Katakana nor Kanji. All of the translations I will make in this exercise will be primarily sourced from machine translation, dictionary lookup or the [walkthrough guide](https://www.giantbomb.com/ray-gun/3030-38838/guide/) for non-Japanese speakers, so bear that in mind.

It won't be a simple one-to-one replacement though; the text will be extracted, studied and re-inserted so that it makes sense - no *"set us up the bomb!"*, as long as I can help it!

---

# Disk Overview

## Disk A / Disk 1

Contents:

  * DISKNO - Contains the bytes 0x00 0x1A
  * COMMAND.X, HUMAN.SYS, AUTOEXEC.BAT - basic Human68k OS (this is a bootable floppy)
  * AI.X, CSS2.X, JISIN.X - The game executables.
  * .MES Files
  * .ATR Files
  * .DAT Files
  * .PR7 Files
  * ANI/.ANI Files
  * PIC/.PR7 Files

### Disk 1 - START.MES

This data file contains the text which is shown at the beginning of the game, immediately after the start screen. This text scrolls up the screen, starting with an image of the town the main character lives in and changing through various images (see below for example).

![Start text](screenshots/start.png)

The section continues through several animated images, including those of your girlfriend being kidnapped by the bad guys of the game. The game proper then begins, with you dropped onto the overworld map. At this point START.MES is no longer used.

All the text in this file relates to that animated intro.

[START.MES](csv/disk1/START.MES.csv) - Japanese to English mapping CSV

---

## Disk B / Disk 2

  * DISKNO - Contains the bytes 0x01 0x1A
  * COMMAND.X, HUMAN.SYS, AUTOEXEC.BAT - basic Human68k OS (this is a bootable floppy)
  * MUSIC.X - FM Synth driver to playback the Ray Gun music tracks
  * RAY_GUN.PCM - ???
  * START.MES - Text for the secret menu and music test screens
  * ANI/.ANI Files
  * PIC/.PR7 Files

## Disk C / Disk 3

  * DISKNO - Contains the bytes 0x02 0x1A
  * START.MES - 
  * ANI/.ANI Files
  * PIC/.PR7 Files
