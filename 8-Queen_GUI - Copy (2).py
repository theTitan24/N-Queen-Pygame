import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('8-Queen Problem')

clock = pygame.Clock()
fps = 30

board = pygame.image.load('board.png').convert()
board = pygame.transform.scale(board, (480, 480))


# Each square 56x56
# Begin at 176, 76

queen = pygame.image.load('bQueen.png').convert_alpha()
queen = pygame.transform.scale(queen, (60, 60))

reticle = pygame.image.load('reticle.png')
reticle.set_colorkey('white')
reticle = pygame.transform.scale(reticle,(56, 56))

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

gridWidth = 56





def getMouseGrid() -> list:
	mousePos = list(pygame.mouse.get_pos())
	mousePos[0] -= 160
	mousePos[1] -= 60
	mouseGrid = [(i // gridWidth) for i in mousePos][::-1]

	return mouseGrid
		
n = 8
pos = [-1 for i in range(n)]

# Game Loop

mouseGrid = [-1, -1]
running = True

while running:
	mousePos = (0,0)
	screen.fill((80, 110, 140))
	screen.blit(board, (160, 60))

	for i in range(n):
		if pos[i] >= 0:
			screen.blit(queen, (174 + (gridWidth*pos[i]), 74 + (gridWidth*i)))


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			print('Mouse Clicked')
			mouseGrid = getMouseGrid()
			print(mouseGrid)
			k = 0

			if (0 <= mouseGrid[0] < n and 0 <= mouseGrid[1] < n):
				pos = [-1 for i in range(n)]
				pos[mouseGrid[0]] = mouseGrid[1]
				k = mouseGrid[0]

				

			if update(pos, 0, n):
				print('Found')
				continue

			
			print('Valid Position Not Found.')
			pos = [-1 for i in range(n)]
			
		
		if event.type == pygame.MOUSEMOTION:
			mouseGrid = getMouseGrid()
	
	if (0 <= mouseGrid[0] < n and 0 <= mouseGrid[1] < n):
		screen.blit(reticle, (174 + (gridWidth*mouseGrid[1]), 74 + (gridWidth*mouseGrid[0])))


	clock.tick(fps)
	pygame.display.flip()

pygame.quit()