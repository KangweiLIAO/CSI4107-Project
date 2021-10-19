package main;

import java.util.*;

public class TokenDoc {
    private final String docID;
    private final ArrayList<String> tokenDocTerms;

    public TokenDoc(String id, ArrayList<String> terms) {
        docID = id;
        tokenDocTerms = terms;
    }

    public ArrayList<String> getTokens() {
        return tokenDocTerms;
    }

    public String getID() {
        return docID;
    }

    @Override
    public String toString() {
        return "TokenDoc{" +
                "docID='" + docID + '\'' +
                ", tokenDocTerms=" + tokenDocTerms +
                '}';
    }
}
