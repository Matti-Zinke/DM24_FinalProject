from typing import List, Union
import random
import os

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

from .base_model import ShopBenchBaseModel

# Set a consistent seed for reproducibility
AICROWD_RUN_SEED = int(os.getenv("AICROWD_RUN_SEED", 3142))


class Mistroll_Cats(ShopBenchBaseModel):
    def __init__(self):
        random.seed(AICROWD_RUN_SEED)

        model_path = 'Qwen/Qwen1.5-MoE-A2.7B-Chat'

        self.tokenizer = AutoTokenizer.from_pretrained('./models/daretires/', trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained('./models/daretires/', device_map='auto',
                                                          torch_dtype=torch.float16, trust_remote_code=True,
                                                          do_sample=True)
        self.system_prompt = "Please listen to the given task carefully and pay special attention on how the answers should be give.\n"
        #self.system_prompt =''
    def predict(self, prompt: str, is_multiple_choice: bool) -> str:
        prompt = self.system_prompt + prompt
        inputs = self.tokenizer(prompt, return_tensors='pt')  # brauch man das??
        inputs.input_ids = inputs.input_ids.cuda()


        if is_multiple_choice:
            if ("Which of the following product") or ("Select the category") in prompt:  # task 2
                prompt = ("You should choose the option which fits best for the given attribute or product "
                          "type. \n\n") + prompt
                print("-------------------2---------------------")
            elif "e-commerce website" and ("total" or "How many") in prompt:  # task 8 // might has to change
                prompt = (("You will be given a product. Answer the given question based on the information "
                           "you have. You have to calculate the answer based on the product name. \n\n") +
                          prompt)
                print("-------------------8---------------------")
            elif "e-commerce website" and ("What type of" or " Is the") in prompt:  # task 5 // maybe have to change
                prompt = ("You will be given a product. Answer the given question based on the information "
                          "you have. \n\n") + prompt
                print("-------------------5---------------------")
            elif "Which of the following statements" in prompt:  # task 11
                prompt = ("You will be given two queries. You have to decide, in which way they are "
                          "related. Take special attention what the general categories of the given queries "
                          "are and how they relate towards each other. \n\n") + prompt
                print("-------------------11---------------------")
            elif "PersonX" in prompt:  # task 9
                prompt = (
                             "You have to make a decision for the given event. The decision should be the most logical cause one would expect. There is always a correct answer, which is never -1.\n\n") + prompt
                print("-------------------9---------------------")
            elif "Which of the following product categories best complement the product type" or "which of the following product categories best complement the given product type?":  # task 10
                prompt = (
                             "You have to choose a category for the following product. The category chosen should be the most complementing for the given product.\n\n") + prompt
                print("-------------------10---------------------")
            elif "Evaluate the following product review on a scale of 1 to 5" in prompt:  # task 15
                prompt = (
                             "You will be given a product and a review given for it. Rate the review on a scale from 1 to 5, with 1 being a very negative review and 5 a very positive review.\n\n") + prompt
                print("-------------------15---------------------")
            elif ("following product" and "following keyword" and "most suitable") or (
                    "following sets of phrases" and "summarize" and "following product") in prompt:  # task 16
                prompt = (
                             "You will be given a product title and description in a foreign language. Choose which of the following categories describes the product the best.\n\n") + prompt
                print("-------------------16---------------------")
            elif (
                    "description" and "exists" and " describe" and "same product" and "different language") in prompt:  # task 18
                prompt = (
                             "You will be given a product with it's description. You have to choose, which of the following products may describe the same product, but in a different language.\n\n") + prompt
                print("-------------------18---------------------")
            elif (
                    "user" and "found" and "description" and "another shopping website in a different language") in prompt:  # task 18
                prompt = (
                             "You will  be given a product description. You have to choose, which of the following descriptions in another language is the most fitting for the given product description. There is always a correct answer, which is never -1.\n\n") + prompt
                print("-------------------18---------------------")
            else:
                prompt = self.system_prompt + "The given question is a multiple choice question. Pay special care on how you should answer.\n\n" + prompt
                print("-------------------ELSE---------------------")
            print("prompt:_----------------------------_" + prompt)
            inputs = self.tokenizer(prompt, return_tensors='pt')
            inputs.input_ids = inputs.input_ids.cuda()
            generate_ids = self.model.generate(inputs=inputs.input_ids, max_new_tokens=1, temperature=1)

        else:
            if " rank " and "product" and "relevance" in prompt:  # task 12
                prompt = ("You have to rank the given products based on the query that is about to be "
                          "mentioned. The way you should answer is described at the end of the "
                          "task. You ALWAYS have to give all 5 numbers.\n\n") + prompt
                print("-------------------12---------------------")
            elif ("xplain " and "category name") or ("xplain " and "product type") or ("ell " and "product category") in prompt:  # task 1
                prompt = ("You have to explain the given product category or type. Your answer should be "
                         "in one sentence of a length of about 20 words.\n\n") + prompt
                print("-------------------1---------------------")
            elif "sentiment" and "potential review" in prompt:  # task 3
                prompt = ("Listen to the given task carefully and pay attention how the formatting will "
                          "be. Take special attention on which kind of product it is and which of the "
                          "reviews fits the aspect that should be mentioned. \n\n") + prompt
                print("-------------------3---------------------")
            elif "extract phrases" in prompt:  # task 4
                prompt = ("Listen to the given task in the next paragraph carefully.  "
                          "Write ONLY the SINGLE most fitting word from the query."
                          "This word should be the best fitting  given entity type in inverted commas.\n\n") + prompt
                print("-------------------4---------------------")
            elif "adequate title" in prompt:  # task 17
                prompt = (
                             "You will be given a product title in inverted commas. You should write the title in the given based on the given context in the language that is mentioned. Do not explain your decisions.\n\n ") + prompt
                print("-------------------17---------------------")
                # You should translate the title into the given language based on how it would appear on an online shopping website.
            elif ("ranslate " and "title" and "into") in prompt:  # task 17
                prompt = ("You will be given a product title in inverted commas. You have to translate it based on the "
                          "language given in the description. You should not explain the answer. \n\n") + prompt
                print("-------------------17---------------------")
            elif "extract the keyphrase" in prompt:  # task 6
                prompt = (
                             "You will be given a review and an aspect. You should generate excatly one short keyphrase based on the given aspect. The keyphrase should only contain the words of the reviewand not be a full sentence. You should not explain the answer or generate other irrelevant text. \n\n") + prompt
            elif "You are given a user review given to a(n) " and "Please choose three aspects from the list that are covered by the review" in prompt:  # task 7
                prompt = (
                             "You will be given a list and a specific review. You should EXACTLY choose 3 aspects as numbers from the given list that are covered in the review and nothing else.\n\n") + prompt
                print("-------------------7---------------------")
            elif ("user" and "sequence" and "queries" and "keyword") in prompt:  # task 13
                prompt = (
                             "Follow the given scenario of you being a user. You just clicked through an online store and made purchases. You are given a query sequence, on which you should guess THREE next most likely queries you would click on, based on your previous interests.\n\n") + prompt
                print("-------------------13---------------------")
            elif ("user" and ("may also buy" or "may also purchase") and "product") in prompt:  # task 14
                prompt = (  "You will be given a product, which just has been bought. Now choose from the following product list EXACTLY 3 products, which are the closest to the given product.\n\n") + prompt
                print("-------------------14---------------------")
            else:
                prompt = self.system_prompt + prompt
                print("-------------------ELSE---------------------")
            print("prompt:_----------------------------_" + prompt)
            inputs = self.tokenizer(prompt, return_tensors='pt')
            generate_ids = self.model.generate(inputs=inputs.input_ids, max_new_tokens=100, temperature=1)

        result = \
        self.tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        generation = result[len(prompt):]

        return generation

    # {"input_field":"A product entitled 'JETech Case for iPad (9.7-Inch, 2018\/2017 Model, 6th\/5th Generation), Smart Cover Auto Wake\/Sleep (Light Purple)' exists on an online shopping website. Generate an adequate title for the product when it appears on a(n) Japanese online shopping website.\nOutput: ","output_field":"JEDirect iPad 9.7\u30a4\u30f3\u30c1 (2018\/2017 \u7b2c6\/5\u4e16\u4ee3\u7528) \u30b1\u30fc\u30b9 PU\u30ec\u30b6\u30fc \u4e09\u3064\u6298\u30b9\u30bf\u30f3\u30c9 \u30aa\u30fc\u30c8\u30b9\u30ea\u30fc\u30d7\u6a5f\u80fd (\u30e9\u30a4\u30c8\u30d1\u30fc\u30d7\u30eb)","task_name":"task17","task_type":"generation","metric":"jp-bleu","is_multiple_choice":false,"track":"amazon-kdd-cup-24-multi-lingual-abilities"}
