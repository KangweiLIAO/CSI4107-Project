package main;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedList;

public class Index {

    private HashMap<String, LinkedList<String>> map;

    public Index(ArrayList<TokenDoc> docs) {
        for (TokenDoc doc : docs) {
            ArrayList<String> tokens = doc.getTokens(); // get tokens from tokenized document
            map = new HashMap<>();
            for (String token : tokens) {
                if (exist(token)) {
                    // if token not in index, put the term into the hashmap:
                    map.put(token, new LinkedList<>());
                } else {
                    // if token in index, append the docID to the term
                    map.get(token).add(doc.docID);
                }
            }
        }
    }

    public boolean exist(String term) {
        return map.getOrDefault(term, null) != null;
    }

    public LinkedList<String> getPosting(String term) {
        return map.get(term);
    }

    public int length() {
        return map.size();
    }
}