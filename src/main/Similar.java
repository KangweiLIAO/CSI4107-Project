package main;

public class Similar implements Comparable<Similar> {
    private double similarity;
    private String docID;

    public Similar(double similarity, String docID) {
        this.similarity = similarity;
        this.docID = docID;
    }

    @Override
    public int compareTo(Similar o) {
        if (this.similarity > o.similarity) {
            return 1;
        } else if (this.similarity == o.similarity) {
            return 0;
        } else {
            return -1;
        }
    }
}
