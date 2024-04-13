from decimal import ROUND_05UP, ROUND_HALF_UP
import math

def center_text(text="aaaa", containerSize=9):
    out = ''
    # start index is center of the container minus text's length divided by 2
    startIndex = math.ceil(containerSize/2) - math.ceil(len(text)/2)
    # add space until the start index is reached
    out += ' ' * startIndex
    # add the actual text
    out += text
    # add the remaining space left on the container
    out += ' ' * (containerSize - len(out))

    return out

print(" ")
print(center_text('xy', 8), center_text('selwyn', 8))
print(center_text('allwyn', 8), center_text('cy', 8))
print(center_text('xy', 8), center_text('selwyn', 8))
print(center_text('allwynsx', 8), center_text('francisc', 8))
print(" ")
