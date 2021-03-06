import gametiles, inventory, random, drawStack

BLOCKLIST = gametiles.BLOCKLIST
PASSABLEBLOCKS = gametiles.PASSABLEBLOCKS
TILEMAP = gametiles.TILEMAP

#COLOR VARIABLES
WHITE   =   (255,255,255)
BLACK   =   (0,0,0)
RED     =   (255,0,0)

PLAYER_SPEED = gametiles.TILESIZE
TILESIZE = gametiles.TILESIZE

class Player():
    def __init__(self):
        self.xpos, self.ypos = 0, 0
        self.inv = inventory.Inventory()
        self.orientation = 0
        #0 - Left
        #1 - UP
        #2 - Right
        #3 - DOWN

    def checkPos(self, x, y):
        if (x//TILESIZE >= gametiles.TILEWIDTH or y//TILESIZE >= gametiles.TILEHEIGHT) or (x < 0 or y < 0):
            return False
        else:
            TargetTile = gametiles.getActiveTile(x, y)
        if not TargetTile.blockid in PASSABLEBLOCKS:
            TargetTile.setBlockID(100)
            return False
        else:return True

    def move(self, dir):
        if dir == "up" and self.checkPos(self.xpos, self.ypos - PLAYER_SPEED):
            self.ypos -= PLAYER_SPEED
            self.orientation = 1
        if dir == "right" and self.checkPos(self.xpos+PLAYER_SPEED, self.ypos):
            self.xpos += PLAYER_SPEED
            self.orientation = 2
        if dir == "left" and self.checkPos(self.xpos-PLAYER_SPEED, self.ypos):
            self.xpos -= PLAYER_SPEED
            self.orientation = 0
        if dir == "down" and self.checkPos(self.xpos, self.ypos+PLAYER_SPEED):
            self.ypos += PLAYER_SPEED
            self.orientation = 3

    def getPos(self):   return self.xpos, self.ypos

    def grabTile(self):
        tile = gametiles.getActiveTile(self.xpos,self.ypos)
        self.inv.addItem(tile.blockid, 1)

    def placeTile(self):
        global BLOCKCOUPLER, NewPlacedTiles
        BLOCKCOUPLER = gametiles.BLOCKCOUPLER
        inv = self.inv
        tile = gametiles.getActiveTile(self.xpos, self.ypos)
        if not inv.isEmpty():
            d = random.choice(list(inv.grabList().keys()))
            if inv.inInv(d):
                try:
                    BLOCKCOUPLER[tile.getBlockID()].remove(tile)
                    inv.removeItem(d, 1)
                    tile.setBlockID(d)
                    if d in BLOCKCOUPLER.keys():
                        BLOCKCOUPLER[d].append(tile)
                    else:
                        BLOCKCOUPLER[d] = [tile]
                    drawStack.stackToDraw.addToStack(tile)
                except:
                    return False
            return True
        else:
            return False

