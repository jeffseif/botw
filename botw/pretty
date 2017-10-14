#! /bin/bash

while read LINE ; do
    echo "${LINE}" \
        | jq \
            --raw-output \
            '
                "> " + .title, (
                    .data
                    | to_entries
                    | sort_by((-1 * .value), .key)
                    | map( [(.value|tostring) + ": " + .key])
                    | .[]
                    | .[]
                )
            ' \
        | sed "s#^\(>.\\+\\)\$#\x1b[1;37m\\1\x1b[0m#" ;
done \
    | less --RAW-CONTROL-CHARS ;
