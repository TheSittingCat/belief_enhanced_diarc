package edu.tufts.hrilab.config.projectConfigs;

import edu.tufts.hrilab.slug.parsing.llm.LLMBeliefUpdater;
import edu.tufts.hrilab.action.GoalManagerComponent;
import edu.tufts.hrilab.nao.MockNaoComponent;

import ai.thinkingrobots.trade.TRADE;
import ai.thinkingrobots.trade.TRADEServiceConstraints;
import ai.thinkingrobots.trade.TRADEServiceInfo;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import edu.tufts.hrilab.diarc.DiarcConfiguration;
import edu.tufts.hrilab.llm.Completion;

public class beliefUpdateLLM extends DiarcConfiguration {
    protected static final Logger LOG = LoggerFactory.getLogger(beliefUpdateLLM.class);

    @Override
    public void runConfiguration() {
        LOG.info("Running the LLM Belief Updater");
        for(TRADEServiceInfo service : TRADE.getAvailableServices()) {
            LOG.info(("Handling service: " + service));
            if(service.equals("UpdateBelief")) {
                try {
                    service.call(String.class);
                }
                catch(Exception e) {
                    LOG.error("Error calling service: " + e.getMessage());
                }
            }
            else {
                LOG.error("Service not found: " + service);
            }
        }
        createInstance(MockNaoComponent.class, "");
        createInstance(GoalManagerComponent.class, "-beliefinitfile llm/llm_test_2.pl -asl beliefexample.asl ");

}
}
