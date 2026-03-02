import pygame

pygame.init()

windowSize = (800, 600)
boardSize = 480

# Change n to make the board bigger or smaller
n = int(input('Board Width (Squares): '))

boardX = (windowSize[0] - boardSize) // 2
boardY = (windowSize[1] - boardSize) // 2
gridWidth = boardSize // n

screen = pygame.display.set_mode(windowSize)
pygame.display.set_caption('8-Queen Problem')

clock = pygame.Clock()
fps = 30

# Load Images

queen = pygame.image.load('bQueen.png').convert_alpha()
queen = pygame.transform.scale(queen, (gridWidth, gridWidth))

reticle = pygame.image.load('reticle.png')
reticle.set_colorkey('white')
reticle = pygame.transform.scale(reticle,(gridWidth, gridWidth))

# Load Font
fontSans = pygame.font.Font('freesansbold.ttf')
topCaption = '- Click on a Square to Place Queen -'
bottomCaption =  "'C': Clear"


# Required Functions

def checkValid(nums: list, n: int):
	for i in range(n):
		if nums[i] < 0:
			continue

		val = nums[i] + 1
		j = i + 1
		while(val < n and j < n):
			if nums[j] == val:
				return False
			val += 1
			j += 1

		val = nums[i] - 1
		j = i + 1
		while(val >= 0 and j < n):
			if nums[j] == val:
				return False
			val -= 1
			j += 1

		val = nums[i] + 1
		j = i - 1
		while(val < n and j >= 0):
			if nums[j] == val:
				return False
			val += 1
			j -= 1

		val = nums[i] - 1
		j = i - 1
		while(val >= 0 and j >= 0):
			if nums[j] == val:
				return False
			val -= 1
			j -= 1
			
	return True

def update(pos: list, rank: int, n: int):
	if rank >= n or rank < 0:
		return True

	if pos[rank] >= 0 and checkValid(pos, n):
		if update(pos, rank + 1, n):
			return True
		return False

	for i in range(n):
		if i in pos:
			continue
		
		pos[rank] = i
		if checkValid(pos, n):
			if update(pos, rank + 1, n):
				return True
		
		pos[rank] = -1

		
	return False

def genBoard(boardSize: int, n: int):

	darkSq = (125, 135, 150)
	lightSq = (232, 235, 239)

	gridWidth = boardSize // n
	board = pygame.Surface((boardSize, boardSize))
	sq = pygame.Rect(0, 0, gridWidth, gridWidth)

	for i in range(n):
		for j in range(n):
			sq.update(j * gridWidth, i * gridWidth, gridWidth, gridWidth)
			if (i + j) % 2 == 0:
				pygame.draw.rect(board, lightSq, sq)
			else:
				pygame.draw.rect(board, darkSq, sq)

	return board

def getMouseGrid(boardX: int, boardY: int, gridWidth: int) -> list:
	mousePos = list(pygame.mouse.get_pos())
	mousePos[0] -= boardX
	mousePos[1] -= boardY
	mouseGrid = [(i // gridWidth) for i in mousePos][::-1]

	return mouseGrid



pos = [-1 for i in range(n)]
board = genBoard(boardSize, n)


# Game Loop

mouseGrid = [-1, -1]
running = True

while running:
	mousePos = (0,0)
	screen.fill((80, 110, 140))

	# Board and Game 

	screen.blit(board, (boardX, boardY))

	for i in range(n):
		if pos[i] >= 0:
			screen.blit(queen, (boardX + (gridWidth*pos[i]), boardY + (gridWidth*i)))


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_c:
				# Clears the Board
				pos = [-1 for i in range(n)]
				topCaption = '- Click on a Square for Solution -'


		if event.type == pygame.MOUSEBUTTONDOWN:
			mouseGrid = getMouseGrid(boardX, boardY, gridWidth)
			# print('Mouse Clicked')
			# print(mouseGrid)
			k = 0

			if (0 <= mouseGrid[0] < n and 0 <= mouseGrid[1] < n):
				pos = [-1 for i in range(n)]
				pos[mouseGrid[0]] = mouseGrid[1]
				k = mouseGrid[0]

				
			
			if update(pos, 0, n):
				topCaption = 'Solution Found !'
				continue

			
			topCation = 'Soltution Not Found'
			pos = [-1 for i in range(n)]
			
		
		if event.type == pygame.MOUSEMOTION:
			mouseGrid = getMouseGrid(boardX, boardY, gridWidth)
	
	if (0 <= mouseGrid[0] < n and 0 <= mouseGrid[1] < n):
		screen.blit(reticle, (boardX + (gridWidth*mouseGrid[1]), boardY + (gridWidth*mouseGrid[0])))

	# UI Elements
	topText = fontSans.render(topCaption, antialias=True, color=(250, 250, 255))
	topTextRect = topText.get_rect(center=(windowSize[0] // 2, boardY // 2))

	bottomText = fontSans.render(bottomCaption, antialias=True, color=(230, 245, 250))
	bottomTextRect = bottomText.get_rect(center=(windowSize[0] // 2, windowSize[1] - boardY//2))

	screen.blit(topText, topTextRect)
	screen.blit(bottomText, bottomTextRect)
	


	clock.tick(fps)
	pygame.display.flip()

pygame.quit()