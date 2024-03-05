from load_settings import*

lines = [
    "+------------------------------------------------+",
    "|  Intelligent Traffic Light System with Traffic |",
    "|              Violation Tracking                |",
    "+------------------------------------------------+",
    "|                     ITLS                       |",
    "+------------------------------------------------+",
    "|                  03/03/2024                    |",
    "+------------------------------------------------+"
]
console_output = "\n".join(lines)
print(console_output)

ROI_1, ROI_2,ROI_3  = level_ROI_cords()

print(ROI_1)
print(ROI_2)
print(ROI_3)