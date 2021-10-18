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
                if (!termExist(token)) { // if token not in index, put the term into the hashmap
                    termMap.put(token, new LinkedList<>(List.of(tmp)));
                    freqMap.put(token, 1);
                } else { // if token in index, append the docID, tf value to the corresponding term
                    freqMap.replace(token, freqMap.get(token) + 1); // update freqMap for the term
                    termMap.get(token).add(tmp);
                }
            }
        }
    }

    /**
     * @param term a word
     * @param doc  a {TokenDoc} instance
     * @return the TF value of this word in this document
     */
    private double computeTF(String term, TokenDoc doc) {
        double nij = 0;
        for (String words : doc.getTokens()) {
            if (words.equalsIgnoreCase(term)) nij++;
        }
        return BigDecimal.valueOf(nij / doc.getTokens().size())
                .setScale(3, RoundingMode.HALF_UP).doubleValue();
    }

    /**
     * @param term a word
     * @return true if the term exist in inverted index, false otherwise.
     */
    public boolean termExist(String term) {
        return termMap.getOrDefault(term.toLowerCase(), null) != null;
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
     * @param term  a word
     * @param docID a specified docID
     * @return the tf-idf weight of the word in docID using raw tf
     */
    public double getWeight(String term, String docID) {
        term = term.toLowerCase();
        return getTF(term, docID) * Main.log(10
                , (double) numOfDocs / getFrequency(term));
    }

    /**
     * @param term  a word
     * @param docID a specified docID
     * @return the TF value of the term in specified doc
     * @throws NullPointerException if the word is not found in inverted index map
     */
    public Double getTF(String term, String docID) throws NullPointerException {
        for (Map.Entry<String, Double> pair : termMap.get(term.toLowerCase())) {
            if (pair.getKey().equals(docID)) {
                return pair.getValue();
            }
        }
        return 0.;
    }

    /**
     * @param term a word
     * @return how many times this word appears in documents
     * @throws NullPointerException if the word is not found in inverted index map
     */
    public Integer getFrequency(String term) throws NullPointerException {
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
    public int length() {
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