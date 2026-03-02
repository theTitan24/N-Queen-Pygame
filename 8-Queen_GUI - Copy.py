import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('8-Queen Problem')

clock = pygame.Clock()

board = pygame.image.load('board.png').convert()
board = pygame.transform.scale(board, (480, 480))


# Each square 56x56
# Begin at 176, 76

queen = pygame.image.load('bQueen.png').convert_alpha()
queen = pygame.transform.scale(queen, (60, 60))

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

def update(pos: list, rank: int, n: int, back: bool = False):
    if rank >= n or rank < 0:
        return True
    
    for i in range(n):
        if i in pos:
            continue
        
        pos[rank] = i
        if checkValid(pos, n):
            if update(pos, rank + 1, n):
                return True
        
        pos[rank] = -1

        
    return False
        
n = 8
pos = [5, -1, -1, -1, -1, -1, -1, -1]

update(pos, 1, n)


running = True

while running:
	screen.fill((80, 110, 140))

	for i in range(n):
		if pos[i] >= 0:
			board.blit(queen, (14 + (56*pos[i]), 14 + (56*i)))


	screen.blit(board, (160, 60))
	# screen.blit(queen, (176 + 56, 76))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	clock.tick(30)
	pygame.display.flip()

pygame.quit()