package main;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

public class TokenDoc {
    String docID;
    ArrayList<String> TokenDocTerms;

    public TokenDoc(String id, ArrayList<String> terms) {
        docID = id;
        TokenDocTerms = terms;
    }

    public void setID(String id) {
        this.docID = id;
    }

    public String getID() {
        return docID;
    }

    public ArrayList<String> getTokens() {
        return TokenDocTerms;
    }
}
