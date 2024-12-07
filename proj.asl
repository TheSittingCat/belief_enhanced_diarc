import java.lang.String;
import edu.tufts.hrilab.fol.Symbol;
import edu.tufts.hrilab.fol.Term;
import edu.tufts.hrilab.fol.Predicate;

import edu.tufts.hrilab.llm.Completion;
import edu.tufts.hrilab.llm.Message;
import edu.tufts.hrilab.llm.Chat;
import edu.tufts.hrilab.llm.Prompts;
import edu.tufts.hrilab.llm.Prompt;

() = llmProj() {
  op:log("info", "llmProj()");
  String !message = "Given the [belief system], generate a one line summary of the action taken.";

  Prompt !prompt = op:newObject("edu.tufts.hrilab.llm.Prompt", !message);
  Completion !res = act:chatCompletion(!prompt);
  op:log("info", "got res");
  String !text = op:invokeMethod(!res, "getText");
  java.util.List !codeList = op:invokeMethod(!res, "getCode");
  String !code;

  if (~op:isEmpty(!codeList)) {
    !code = op:invokeMethod(!codeList, "get", 0);
    op:log("info", "Got code");
    op:log("info", !code);
  } else {
    op:log("info", "Did not get code");
    op:log("info", !text);
  }
}

