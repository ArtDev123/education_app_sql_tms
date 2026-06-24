def is_valid_int(value: str) -> bool:
    if not isinstance(value, str) or not value:
        return False
    
    # Убираем знак минус в начале, если он есть, и проверяем, что остались только цифры
    if value[0] == '-':
        return value[1:].isdigit()
        
    return value.isdigit()