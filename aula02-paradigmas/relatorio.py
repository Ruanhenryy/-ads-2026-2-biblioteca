VENDAS = [   
    {"produto": "Teclado",  "valor": 150.00, "categoria": "Periferico"},
    {"produto": "Mouse",    "valor":  80.00, "categoria": "Periferico"},
    {"produto": "Monitor",  "valor": 900.00, "categoria": "Tela"},
    {"produto": "Cabo HDMI","valor":  35.00, "categoria": "Acessorio"},
    {"produto": "Headset",  "valor": 250.00, "categoria": "Periferico"},    
    {"produto": "Suporte",  "valor": 120.00, "categoria": "Acessorio"}
    ] 

IMPOSTO = 0.10 
VALOR_MINIMO = 100.00 

def relatorio(vendas):   
    """Total liquido por categoria, apenas de vendas acima do minimo."""    
    total_por_categoria = {}    

    for v in vendas:        
        if v["valor"] <= VALOR_MINIMO:            
            continue        

        liquido = v["valor"] * (1 - IMPOSTO)        
        cat = v["categoria"]        

        if cat not in total_por_categoria:            
            total_por_categoria[cat] = 0        
        total_por_categoria[cat] += liquido   

    return total_por_categoria



if __name__=="__main__":
    for categoria, total in relatorio(VENDAS).items():        
        print(f"{categoria:12} R$ {total:8.2f}")