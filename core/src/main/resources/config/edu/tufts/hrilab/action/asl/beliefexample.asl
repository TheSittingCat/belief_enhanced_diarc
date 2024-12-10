import edu.tufts.hrilab.fol.Symbol;

() = move(Symbol ?pose, Symbol ?place1, Symbol ?place2, Symbol ?place3) {
    op:log("info", "?actor received ?pose and ?place1, ?place2, ?place3");
    act:goToPosture(?pose);
    act:moveTo(?place1, ?place2, ?place3);
}