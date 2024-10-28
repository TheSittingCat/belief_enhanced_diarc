package edu.tufts.hrilab.slug.parsing.llm;

import ai.thinkingrobots.trade.TRADEService;
import ai.thinkingrobots.trade.TRADEServiceConstraints;
import ai.thinkingrobots.trade.TRADE;
import edu.tufts.hrilab.slug.parsing.llm.LLMParserComponent;
import edu.tufts.hrilab.llm.Completion;

public class BeliefParserComponent extends LLMParserComponent {
    public BeliefParserComponent() {
        super();
    }

    @TRADEService
    public String GetDirectLLM(String Input) { 
        String response_llm;
        String prompt = "Who are you?";
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
        return response_llm;
    }
}
