from openai import OpenAI
client = OpenAI()

def get_completion(prompt, model="gpt-4o-mini"):
  response = client.chat.completions.create(
  model=model,
  messages = [
    {"role": "system", "content": "You are a maps and addresses expert"}, 
    {"role": "user", "content": prompt}
  ]
)
  return response.choices[0].message.content


def find_valid_address(address_list):
  prompt = f"""
    The list {address_list} contains potential address found on a business website. A \
    regex pattern has recognized this list. The list items might contain some junk text \
    or it might contain an address in a pure form, or an addressalong with some junk text. Your job is to \
    recognize an address if there is any, and return that.

    output format:
    the found address or None

    additional info: Don't waste my tokens on extra info, simply return the found address or None."""
  
  return get_completion(prompt)
  
  


# addresses = ['book a VERSACLIMBER classsTopCall us today at304-550-8660108 Capitol Street, Charleston, WV 25301']



# response, total_tokens = get_completion(prompt)
# print(response)
# print(total_tokens)


