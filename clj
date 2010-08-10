#!/bin/sh
# use autocompletion with clojure with rlwrap

breakchars="(){}[],^%$#@\"\";:''|\\"
CLOJURE_DIR=/opt/local/share/java/clojure/lib/
CLOJURE_JAR="$CLOJURE_DIR"/clojure.jar
if [ $# -eq 0 ]; then 
    exec rlwrap --remember -c -b "$breakchars" \
        -f "$HOME"/.clj_completions \
        java -cp "$CLOJURE_JAR" clojure.main --repl
else
    exec java -cp "$CLOJURE_JAR" clojure.main $1 -- "$@"
fi