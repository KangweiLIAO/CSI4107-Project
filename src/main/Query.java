package main;

import java.util.ArrayList;

public class Query {
    public String Qid = "-1";
    public ArrayList<String> queryTerms;

    // Default Constructor
    public Query() {
    }

    // Constructor
    public Query(String Qid, ArrayList<String> queryTerms) {
        Qid = Qid;
        queryTerms = queryTerms;
    }

    public void setQid(String id) {
        this.Qid = id;
    }

    public String getQid() {
        return Qid;
    }

    public void setQueryTerms(ArrayList<String> queryTerms) {
        this.queryTerms = queryTerms;
    }

    public ArrayList<String> getQueryTerms() {
        return queryTerms;
    }
}
