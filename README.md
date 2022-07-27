# Dolby SR•D
An effort to reverse engineer Dolby SR•D, ie. Dolby Digital on 35mm film

---

In 1991[^1] Dolby Laboratories introduced **Dolby Digital** (or _Spectral Recording Dolby Stereo Digital_, aka SR•D, as it was known at the time. This was a new sound format for 35mm film, consisting of two parts:
1. An audio compression technique to reduce the storage requirements of 6 channels of audio
2. A physical encoding of the compressed audio onto 35mm film

Dolby Digital was the most popular digital soundtrack on 35mm film throughout the 90s and 2000s, and although as of 2013 onwards 35mm has become a rarity, Dolby Digital still remains in use for modern film releases (such as _Licorice Pizza_ in 2021 and _Doctor Strange in the Multiverse of Madness_ in 2022).

Although Dolby published the audio compression specification as AC3 or ATSC A/52 [^2], and the last patents of Dolby Digital expired a few years ago[^3], the physical encoding of Dolby Digital on film has never been released, or reverse engineered. This project therefore exists to share information discovered and reverse engineered about Dolby Digital on film.

---

This repository has two sections:
1. A [publically editable wiki](https://github.com/davidferguson/dolby-srd/wiki) documenting information about the Dolby SR•D format, as well as the equipment used to encode/decode/process it
2. Files relating to the reverse engineering effort, including equipment manuals, logic capture dumps, utility programs, etc.

**Any help is most welcome! Especially for file format/signal analysis. Have a look at the [current work/status]() wiki page to see how you can get involved.**

[^1]: The first demonstrations of Dolby Digital on 35mm were made in April 1991, but it wasn't until 1992 with _Batman Returns_ that a film was released using it.
[^2]: https://www.atsc.org/wp-content/uploads/2016/03/a_52-2015.pdf
[^3]: https://news.ycombinator.com/item?id=13910925#:~:text=The%20last%20patent%20on%20AC,expires%20at%20midnight%20%7C%20Hacker%20News&text=We%20in%20North%20America%20have,standard%20for%20MPEG%2D2%20DVDs.
