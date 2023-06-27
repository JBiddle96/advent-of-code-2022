input_file = "input.txt"

with open(input_file, "r") as f:
    input_list = f.readlines()

input_list.append("\n")  # Ensure the final total is added

elf_list = []
current_sum = 0
for num in input_list:
    if num != "\n":
        current_sum += int(num.rstrip())
    else:
        elf_list.append(current_sum)
        current_sum = 0

print(max(elf_list))

sorted_elf_list = sorted(elf_list, reverse=True)
print(sorted_elf_list[0:3])
print(sum(sorted_elf_list[0:3]))
