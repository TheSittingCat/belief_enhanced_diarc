package edu.tufts.hrilab.slug.parsing.llm;

import ai.thinkingrobots.trade.TRADEService;
import ai.thinkingrobots.trade.TRADEServiceConstraints;

import com.google.api.client.json.webtoken.JsonWebSignature.Parser;

import ai.thinkingrobots.trade.TRADE;
import edu.tufts.hrilab.slug.parsing.llm.LLMParserComponent;
import edu.tufts.hrilab.llm.Completion;
import edu.tufts.hrilab.fol.Symbol;

public class BeliefParserComponent extends LLMParserComponent {
    public BeliefParserComponent() {
        super();
    }

    @TRADEService
    public AlternateResponse GetDirectLLM(String Input) { 
        String response_llm;
        String prompt = Input;
        ParserResponse alt = new ParserResponse();
        alt.referents = new Referent[0];
        alt.descriptors = new Descriptor[0];
        alt.intention = new Intention();
        log.warn("Hello from BeliefParserComponent");
        try {
            log.warn("Please Wait for the response from LLM, this can take several seconds");
            response_llm = TRADE.getAvailableService(new TRADEServiceConstraints().name("chatCompletion").argTypes(String.class)).call(Completion.class,prompt).getText();
            log.warn("Response from LLM: " + response_llm);
        }

        catch (Exception e) {
            log.info(e.getMessage());
            response_llm = Input;
        }
        alt.intention.intent = "INSTRUCT";
        alt.intention.proposition = new Proposition();
        alt.intention.proposition.text = response_llm;
        alt.intention.proposition.type = "action";
        alt.intention.proposition.arguments = new String[0];
        return new AlternateResponse(alt, new Symbol("GPT-4o"));
    }
}
