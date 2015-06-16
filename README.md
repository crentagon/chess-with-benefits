# Chess With Benefits 

Chess With Benefits: Chess made much friendlier.

-----------------------

## Introduction

- **Motivation**: Not a lot of people play chess nowadays due to its level of difficulty, especially when positions get very complicated.
- **Objective**: To get people to play chess more by adding certain features into the game that make it easier for casual players to play. 

-----------------------

## Technical Specifications

- [Python 2.7](https://www.python.org/ftp/python/2.7/python-2.7.amd64.msi)
- [PyGame 1.9.1](http://pygame.org/ftp/pygame-1.9.1.win32-py2.7.msi)

-----------------------

## Major Features

1. **Heat Map**

	1. Greatly aids players decide their moves.
	2. In the following photo, the tile says “3” in blue, because three of the player’s pieces are defending the tile.

	![heatmap-001](https://github.com/crentagon/chess-with-benefits/blob/master/res/heatmap-001.png)
	
	3. The tile says “3” in red, because three of the opponent’s pieces are defending the tile.

	![heatmap-002](https://github.com/crentagon/chess-with-benefits/blob/master/res/heatmap-002.png)

	4. The tile says “1” in red, because there 3 of the opponent’s pieces are defending the tile, while there are only 2 user pieces attacking the same tile – the numbers are cumulative.

	![heatmap-003](https://github.com/crentagon/chess-with-benefits/blob/master/res/heatmap-003.png)

	5. Note that the numbers are cumulative.

2. **HP Display**

	1. Helps players become aware of the values of pieces: “Is sacrificing this piece for that piece a worthy sacrifice?”

	2. Note that the piece values are:

	![piece-values-01](https://github.com/crentagon/chess-with-benefits/blob/master/res/piece-values-01.png)

3. **Piece Status**

	1. Aids players by showing important information of a piece upon right-clicking it.

	![piece-status-01](https://github.com/crentagon/chess-with-benefits/blob/master/res/piece-status-01.png)

	2. Major Statuses:

		1. **Tiles Controlled**: Number of tiles it can travel to (and thus the opponent can’t travel to, to avoid getting taken).

		2. **Offensive Power**: Number of enemy pieces it is attacking.

		3. **Defensive Power**: Number of friendly pieces it is defending.

		4. **Attackers**: Number of pieces attacking it.

		5. **Defenders**: Number of pieces defending it.

		6. **Status**:

			1. **Defender**: Defending at least two pieces
			
			2. **Warrior**: Controlling at least 60% of the maximum possible number of tiles it can control.
			
			3. **Threatened**: Being attacked by a piece without being defended OR being attacked by a piece of lower rank.

			4. **Healthy**: The default status
