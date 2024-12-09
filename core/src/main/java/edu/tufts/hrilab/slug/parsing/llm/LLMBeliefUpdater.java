package edu.tufts.hrilab.slug.parsing.llm;

import ai.thinkingrobots.trade.TRADEService;
import ai.thinkingrobots.trade.TRADEServiceConstraints;

import com.google.api.client.json.webtoken.JsonWebSignature.Parser;

import ai.thinkingrobots.trade.TRADE;
import edu.tufts.hrilab.slug.parsing.llm.LLMParserComponent;
import edu.tufts.hrilab.llm.Completion;
import edu.tufts.hrilab.action.annotations.Action;
import edu.tufts.hrilab.fol.Symbol;

public interface LLMBeliefUpdater {

    @TRADEService
    String ReturnInput();

    @TRADEService
    String ReadBelief();

    @TRADEService
    @Action
    String UpdateBelief();
}
