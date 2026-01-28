import bill_calculator_inputs
import datetime
masked_phone=bill_calculator_inputs.phone[:-5]+"*****"
total_bill=0
for place,amount in bill_calculator_inputs.bill_details:
    total_bill += amount
output_text=""
output_text+="\n--- Person Billing Details ---\n"
output_text+=f"Name     : {bill_calculator_inputs.name}\n"
output_text+=f"Phone No : {masked_phone}\n"
output_text+="\n--- Bill Breakdown ---\n"
for place, amount in bill_calculator_inputs.bill_details:
    output_text+=f"{place}:₹{amount:.2f}\n"
output_text += f"\nTotal Bill : ₹{total_bill:.2f}\n"
print(output_text)
with open(f"output_{datetime.date.today()}.txt", "w", encoding="utf-8") as file:
    file.write(output_text)

