package main;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.*;

/**
 * @author Kangwei Liao
 * <p>
 * Represents inverted indexing, stored using hashmap.
 */
public class Index {

    private final int numOfDocs;
    private final HashMap<String, LinkedList<Map.Entry<String, Double>>> termMap; // HashMap<term, LinkedList<Map.Entry<docID, weight>>>
    private final HashMap<String, Integer> freqMap; // HashMap<term, frequency>
    private final HashMap<String, TokenDoc> docMap; // HashMap<term, docSize>

    /**
     * Constructor of Index class, base on the input documents output an inverted index map
     *
     * @param docs a list of {TokenDoc} instance to initialize an inverted index instance
     */
    public Index(ArrayList<TokenDoc> docs) {
        numOfDocs = docs.size();
        termMap = new HashMap<>();
        freqMap = new HashMap<>();
        docMap = new HashMap<>();
        for (TokenDoc doc : docs) {
            // System.out.println("34952194402811904");
            docMap.put(doc.getID(), doc);
            ArrayList<String> tokens = doc.getTokens(); // get tokens from tokenized document
            for (String token : tokens) {
                token = token.toLowerCase();
                Map.Entry<String, Double> tmp = new AbstractMap.SimpleEntry<>(doc.getID(), computeTF(token, doc)); // (docID, TF) pair for a term
                if (termExist(token)) { // if token not in index, put the term into the hashmap
                    termMap.get(token).add(tmp);
                } else { // if token in index, append the docID, tf value to the corresponding term
                    termMap.put(token, new LinkedList<>(List.of(tmp)));
                    if (freqMap.get(token) == null) {
                        freqMap.put(token, 1);
                    } else {
                        freqMap.replace(token, freqMap.get(token) + 1); // update freqMap for the term
                    }
                }
            }
        }
    }

    /**
     * @param term a word
     * @param doc  a {TokenDoc} instance
     * @return the TF weight of this word in this document
     */
    private double computeTF(String term, TokenDoc doc) {
        double rawTF = 0.;
        for (String words : doc.getTokens()) {
            if (words.equalsIgnoreCase(term)) rawTF++;
        }
        if (rawTF == 0) return 0;
        return 1 + Main.log(10, rawTF);
    }

    /**
     * @param term  a word
     * @param docID a specified docID
     * @return the TF value of the term in specified doc
     * @throws NullPointerException if the word is not found in inverted index map
     */
    public double getTF(String term, String docID) throws NullPointerException {
        if (!termExist(term)) return 0;
        for (Map.Entry<String, Double> pair : termMap.get(term.toLowerCase())) {
            if (pair.getKey().equals(docID)) {
                return pair.getValue();
            }
        }
        return 0;
    }

    /**
     * @param term  a word
     * @param docID a specified docID
     * @return the tf-idf weight of the word in docID using raw tf
     */
    public double getTFIDF(String term, String docID) {
        term = term.toLowerCase();
        if (!termExist(term)) return 0;
        return getTF(term, docID) * Main.log(10
                , (double) numOfDocs / getFrequency(term));
    }

    /**
     * @param term a word
     * @return true if the term exist in inverted index, false otherwise.
     */
    public boolean termExist(String term) {
        return termMap.get(term.toLowerCase()) != null;
    }

    /**
     * @param term a word
     * @return the posting of the word
     * @throws NullPointerException if the word is not found in inverted index map
     */
    public LinkedList<Map.Entry<String, Double>> getPosting(String term)
            throws NullPointerException {
        return termMap.get(term.toLowerCase());
    }

    /**
     * @return the total number of document in this inverted index map
     */
    public int getNumOfDocs() {
        return numOfDocs;
    }

    /**
     * @param term a word
     * @return how many times this word appears in documents
     * @throws NullPointerException if the word is not found in inverted index map
     */
    public int getFrequency(String term) throws NullPointerException {
        return freqMap.get(term.toLowerCase());
    }

    /**
     * @param docID document ID
     * @return return the {TokenDoc} instance with docID
     */
    public TokenDoc getDoc(String docID) {
        return docMap.get(docID);
    }

    /**
     * @return the length (number of terms) of the inverted index map
     */
    public int numOfTerms() {
        return termMap.size();
    }

    @Override
    public String toString() {
        StringBuilder result = new StringBuilder();
        for (Map.Entry<String, LinkedList<Map.Entry<String, Double>>> entry : termMap.entrySet()) {
            String term = entry.getKey();
            result.append("{").append(term).append("(").append(getFrequency(term)).append(") : ");
            for (Map.Entry<String, Double> pair : entry.getValue()) {
                result.append("[").append(pair).append("], ");
            }
            result.append("}");
        }
        return result.toString();
    }
}