# a ="""Who can warm me up, who else
# loves?
# Stretch out your hot hands
# And the flame of glowing coals for the heart
# give.
# I lie powerless, numb from fear,
# As before death, when the legs
# freeze
# Trembling in fits of evil, unknown
# illness
# And trembling under the sharp ends
# Your cold, freezing arrows.
# You are hunting me, thoughts spirit,
# Shrouded, terrible, nameless -
#
# Hunter from behind the clouds! -
# Like lightning, I am struck by the eye,
# Mockingly looking out of the dark!
# And so I lie, wriggling,
# Bent over, crooked, tortured
# ferociously
# By the torment that you sent me
# Ruthless hunter
# God unknown to me! - """
# #
# a = a.replace("!", " ")
# a = a.replace(",", " ")
# a = a.replace(".", " ")
# a = a.replace("?", " ")
# a = a.replace("-", " ")
# a = a.split()
#
# print(a)
# print(len(a))
#
# print("Ноль индекс - ", a[30], a[4], a[82], a[99], a[42], a[80], a[87])
# print("Один индекс - ", a[31], a[5], a[83], a[100], a[43], a[81], a[88])
# print("Ноль индекс - ", a[30] + a[4] + a[82] + a[99] + a[42] + a[80] + a[87])
# print("Один индекс - ", a[31] + a[5] + a[83] + a[100] + a[43] + a[81] + a[88])
# # for i, j in enumerate(a):
# #     print(a[30-i], a[4-i], a[82-i], a[99-i], a[42-i], a[80-i], a[87-i])
#
# print(a[30][0] + a[4][0] + a[82][0] + a[99][0] + a[42][0] + a[80][0] + a[87][0])
# print(a[31][0] + a[5][0] + a[83][0] + a[100][0] + a[43][0] + a[81][0] + a[88][0])
# #print(Beaufort("hbtftso").decipher("RuxofZsg+GHJey+sICeP9WIlmg8mI/1G"))
# #print(set(a))
# #print(len(set(a)))
line = "3439373432303639373332303734363836353230373037323639373636393643363536373635323036463636323037343638363532303637364636343733323037343646323037373631364537343230364536463734363836393645363732433230363136453634323036463636323036373646363436433639364236353230364436353645323037343646323037373631364537343230364336393734373436433635304430413044304136373644364637413643373437333736373637373632373236333732363536433634373836343732363936363245364237333044304130443041353032453533324532303639324536393644363737353732324536333646364432463733353834443431333033323535324536413730363732303244334532303532344635343330"
n = 2
line = [line[i:i+n] for i in range(0, len(line), n)]
print(sorted(set(line)))