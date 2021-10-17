package main;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
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
}
