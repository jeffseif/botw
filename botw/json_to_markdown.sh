#! /bin/bash

while read LINE ; do
    echo "${LINE}" \
        | jq \
            --raw-output \
            '
                "# " + .title + "\n", (
                    .data
                    | to_entries
                    | sort_by((-1 * .value), .key)
                    | map( ["- " + (.value|tostring) + ": " + .key])
                    | .[]
                    | .[]
                )
            ' ;
    echo ;
done \
    | sed '$d' ;
