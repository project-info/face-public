from simple_facerec import SimpleFacerec
import json

# Encode faces from a folder
sfr = SimpleFacerec()
sfr.load_encoding_images("newImages/")

comparisons = sfr.comparisons()
with open('./comparisons.json', 'w', encoding='utf-8') as f:
    json.dump(comparisons, f, ensure_ascii=False, indent=4)

contrasts = sfr.contrasts()
with open('./contrasts.json', 'w', encoding='utf-8') as f:
    json.dump(contrasts, f, ensure_ascii=False, indent=4)

print(sfr.compare_face("Daphne Huang '25", "Julie Yan '26"))