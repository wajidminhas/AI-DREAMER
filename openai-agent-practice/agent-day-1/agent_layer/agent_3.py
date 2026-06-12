from agents import input_guardrail, GuardrailFunctionOutput

@input_guardrail
async def block_bad_words(ctx, agent, input_data):
    
    text = str(input_data).lower()
    
    if "hack" in text or "malware" in text:
        return GuardrailFunctionOutput(
            output_info="Bad word detected",
            tripwire_triggered=True   
        )
    
    return GuardrailFunctionOutput(
        output_info="OK",
        tripwire_triggered=False      
    )