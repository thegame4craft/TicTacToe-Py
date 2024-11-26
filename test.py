from MiniMax import MiniMax
from Field import Field

field = Field()

# generate a field
"""
X _ O
_ X _
X O _
"""
field.place(0, 0, "O")
field.place(0, 1, "O")
field.place(0, 2, "O")

mm = MiniMax(field, "O")
br = mm.basic_rate(field)
end, root = mm.build_tree("O")
rating = mm.rate_tree(root)
print(root)