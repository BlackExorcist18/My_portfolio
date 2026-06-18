# 3. List comprehension (работа со строками)
words = ["python", "Java", "c++", "Rust", "go"]
filtered_words = [word.upper() for word in words if len(word) > 3]
print("3. Слова в верхнем регистре длиннее 3 символов:", filtered_words)