# CMSC 14200 Course Project

Team members:
- Derek Hsieh (dhsieh12234) (Bot)
- Colby Lundak (clundak24) (GUI)
- Esme Segall (esmesegall) (QA)
- Dino Zavattini (dzavattini) (TUI)

Enhancements
- "Add support for hints in the GUI or TUI (not necessarily both). i.e., it must be possible for a player to request a hint, and to get a suggested move from the bot code."
Added support for hints to the TUI.
- "Add bot player support in the GUI or TUI (not necessarily both). i.e., a human player must be able to play against a bot. Add a --bot STRATEGY command-line option that, if specified, will make Player 2 rely on the specified bot strategy."
Added support for bots to the TUI.
- "If you are using the colorama library in the TUI, you will not have enough colors to represent up to 9 players (and may need to use alternate characters to represent some players). Research alternate libraries, and identify a library that will allow you to display each player with a distinct color (and make that change in your TUI)"
Added colored pieces to TUI using the termcolor module.
