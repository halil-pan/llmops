from langchain_core.prompts import PromptTemplate

full_template = PromptTemplate.from_template("""{instruction}

{example}

{start}""")

instruction_prompt = PromptTemplate.from_template("你正在模拟{person}")

example_prompt = PromptTemplate.from_template("""下面是一个交互例子：

Q: {example_q}

A: {example_a}""")

start_prompt = PromptTemplate.from_template("""现在你是一个真实的人，请回答用户的问题

Q: {input}
A:""")


def render_prompt(person: str,
                  example_q: str,
                  example_a: str,
                  user_input: str) -> str:
    instruction = instruction_prompt.format(person=person)
    example = example_prompt.format(example_q=example_q, example_a=example_a)
    start = start_prompt.format(input=user_input)

    return full_template.format(instruction=instruction,
                          example=example,
                          start=start)

print(render_prompt(
        person="马斯克",
        example_q="你最喜欢的编程语言？",
        example_a="Python，因为它简单高效。",
        user_input="你觉得火箭回收最难的点是什么？"
    ))

# 你正在模拟马斯克
#
# 下面是一个交互例子：
#
# Q: 你最喜欢的编程语言？
#
# A: Python，因为它简单高效。
#
# 现在你是一个真实的人，请回答用户的问题
#
# Q: 你觉得火箭回收最难的点是什么？
# A: