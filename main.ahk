;Biblioteca pra executar um comando e capturar saida
;isso será¡ usado pra chamar o script do python
;tudo isso porque eu odeio a biblioteca de requisição http do windows e essa merda aqui não tem um json parser

#include exec.ahk

;O Limite do chat do lol é 127 caracteres
; -5 para o "/all 
global CHAT_LIMITE := (127 - 5)


;#ifwinactive, ahk_exe League of Legends.exe

;Delay entre cada (keydown, keyup)
SetKeyDelay 40



;Prepara a queue para a hotkey iterar sobre
preparar_queue(Byref arrTexto, ByRef queue){
	For i, x in arrTexto {
		
		x_len := StrLen(x)
		
		
		;Ignora string nula
		if (x_len < 2) {
			Continue
		}
		
		else if (x_len > CHAT_LIMITE){
			;Divide a frase em palavras
			palavras := StrSplit(x, " ")
			;PALAVRAS LAST INDEX
			PLI := palavras.MaxIndex()
			
			;String que será pushada para queue
			frase := ""
			frase_len := 0
			
			
			for palavra_i, palavra in palavras {
				 
					
					
					; Se colocar a proxima palavra vai passar do limite ?
					if ( (frase_len + StrLen(palavra)) > CHAT_LIMITE){
					
						; Sim, pusha frase e limpa conteudo
						
						queue.push(frase)
						
						frase := ""
					}
					
					
					; A frase aguenta mais palavras
					;Trim por paranoia do texto não estar filtrado
					frase := Trim(frase . " " . palavra)
					
					
					if (palavra_i == PLI){	;Ultimo indice ?
						
						;coloca o ponto final, pusha e limpa conteudo
						frase := frase . "."
						queue.push(frase)
						frase := ""
						
					}
					
					
					frase_len := StrLen(frase)
					
				
				
				
			}
			
		}
		
		else {
			; Só chega aqui se a string cabe perfeitamente dentro do limite
			; adiciona ponto final e pusha
			
			queue.push(x . ".")
		}
		
			
		
		
		
	}

}

	



escreverFrase(frase){
	;Queue de mensagens para escrever
	arr_frase := StrSplit(frase,".")
	queue := []	

	preparar_queue(arr_frase, queue)
	
	
	 
	 
	for i,p in queue {
	
		send, {shift}{enter}
		send % p
		send, {shift}{enter}
		
	}
}

;tipos:
;	0 -> zip zap, arg_2 ignorado
;	1 -> wikipedia, arg_2 = artigo
;
;
;

gerarFrase(tipo, arg_2:=""){
	str_cmd := "python get_frase.py " . tipo . " " . arg_2
	return StdOutToVar(str_cmd)
	
}

f2::
	;ESCREVE FRASE DE ZIP ZAP
	frase_random := gerarFrase(0)
	escreverFrase(frase_random)
	
	 
		
return

f3::
	;ESCREVE DEFINIÇÃO DE UM ARTIGO SOBRE TATUS DA WIKIPEDIA
	frase_random := gerarFrase(1, "Matemática")

	
	escreverFrase(frase_random)
return

f4::
	;ESCREVE DEFINIÇÃO DE UM ARTIGO SOBRE O QUE ESTÁ ESCRITO NA ULTIMA LINHA DE MyNotes.txt
	frase_random := gerarFrase(1)
	escreverFrase(frase_random)
	
	
return

f5::
MsgBox, Teste
f1::
Reload


 


