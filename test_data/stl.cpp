/*
 * Let's use the Standard Template Library!
 * */
#include <iostream>
#include <string>
#include <vector>
#include <list>
#include <algorithm>

using namespace std;


/*
 * Make a template for a print_list that can handle
 * lists of any type:
 * */
template <typename T>
void print_list(const string name, const list<T>& l) {
    cout << "\n_______" << endl;

    cout << name << ":\n";
    for (T item : l) cout << item << " ";

    cout << "\n_______" << endl;
}


/*
 * But, we can go even more generic, and make a print that can print
 * *containers* of any type:
 * */
template <typename SequenceContainer>
void print(const string name, const SequenceContainer& seq) {
    cout << "\n_______" << endl;
    cout << name << ":\n";
    for(auto& item : seq) cout << item << " ";
    cout << "\n_______" << endl;
}


/*
 * We could pass this `is_odd()` function in to a `find_if()`,
 * or pass a lambda instead.
 * */
bool is_odd(int n) { return (n % 2) != 0; }


int main() {
    int bjarnelen = 17;
    int dennislen = 14;

    char s[]  = "Bjarne Stroustrup";
    char s2[] = "Dennis Ritchie";

    cout << "C++ creator: " << s << "\n";
    cout << "C creator, 4th letter: " << s2[3] << "\n";

    /*
     * Let's do some things with a vector.
     * */
    vector<char> cvec(s2, s2 + dennislen);
    print("cvec", cvec);
    sort(cvec.begin(), cvec.end());
    print("sorted cvec", cvec);

    /*
     * char list:
     * */
    list<char> clist(s, s + bjarnelen);
    list<char> clist2 = clist;
    /*
     * The STL provides us with a `reverse()` functions that
     * reverses an iterable structure:
     * */
    reverse(clist.begin(), clist.end());
    // We use print_list here just to make sure it works, but print()
    // is preferred!
    print_list("clist reversed", clist);
    /*
     * But even after `clist` is reversed, `clist` and
     * `clist2` are still permutations of each other:
     * */
    cout << "Is clist a permutation of clist2? "
        << is_permutation(clist.begin(), clist.end(), clist2.begin())
        << endl; ;

    /*
     * int list:
     * */
    int ilen = 8;
    int iptr[] = { 16, 32, 64, 128, 2, 4, 8, 17 };
    list<int> ilist(iptr, iptr + ilen);
    // Our print can work for lists as well as vectors:
    print("ilist", ilist);
    /*
     * `sort()` does not work for lists, since they aren't random access.
     * Thus lists have their own `sort()` method, called below:
     * */
    ilist.sort();
    print("ilist sorted", ilist);

    /*
     * Let's experiment with iterators a bit!
     * */
    list<int>::iterator iiter = find(ilist.begin(), ilist.end(), 8);
    cout << "After find(), iter is at: " << *iiter << endl;
    ++iiter;
    if (iiter != ilist.end()) {
        cout << "After increment, iter is at: " << *(iiter) << endl;
    }

    /*
     * Here we are going to pass `is_odd() to `find_if()`.
     * */
    list<int>::iterator if_iter1 = find_if(ilist.begin(), ilist.end(), is_odd);
    cout << "First is_odd() number in list is: " << *if_iter1 << endl;

    /*
     * Here we are going to pass a lambda to `find_if()`.
     * The lambda starts with []. The point here is to show
     * that this form and the one above are identical in effect.
     * */
    list<int>::iterator if_iter2 = find_if(ilist.begin(),
            ilist.end(), [] (int n) { return (n % 2) != 0; });
    cout << "First lambda odd number in list is: " << *if_iter2 << endl;
}








