(ns gen-maat-log
  (:require
   [babashka.process :as proc]))

(defn gen-log [project-dir out-file]
  (let [proc (proc/sh
              {:dir project-dir}
              "git log --all --numstat --date=short --pretty=format:'--%h--%ad--%aN' --no-renames --after=2019-01-01")]
    (spit out-file (:out proc))))

(gen-log "/home/andrea/src/work/kleene/minoro.kioku" "kioku.log")
