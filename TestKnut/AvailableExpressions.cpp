
#include "souffle/CompiledSouffle.h"

extern "C" {
}

namespace souffle {
static const RamDomain RAM_BIT_SHIFT_MASK = RAM_DOMAIN_SIZE - 1;
struct t_btree_ii__0_1__11__10 {
static constexpr Relation::arity_type Arity = 2;
using t_tuple = Tuple<RamDomain, 2>;
struct t_comparator_0{
 int operator()(const t_tuple& a, const t_tuple& b) const {
  return (ramBitCast<RamSigned>(a[0]) < ramBitCast<RamSigned>(b[0])) ? -1 : (ramBitCast<RamSigned>(a[0]) > ramBitCast<RamSigned>(b[0])) ? 1 :((ramBitCast<RamSigned>(a[1]) < ramBitCast<RamSigned>(b[1])) ? -1 : (ramBitCast<RamSigned>(a[1]) > ramBitCast<RamSigned>(b[1])) ? 1 :(0));
 }
bool less(const t_tuple& a, const t_tuple& b) const {
  return (ramBitCast<RamSigned>(a[0]) < ramBitCast<RamSigned>(b[0]))|| (ramBitCast<RamSigned>(a[0]) == ramBitCast<RamSigned>(b[0])) && ((ramBitCast<RamSigned>(a[1]) < ramBitCast<RamSigned>(b[1])));
 }
bool equal(const t_tuple& a, const t_tuple& b) const {
return (ramBitCast<RamSigned>(a[0]) == ramBitCast<RamSigned>(b[0]))&&(ramBitCast<RamSigned>(a[1]) == ramBitCast<RamSigned>(b[1]));
 }
};
using t_ind_0 = btree_set<t_tuple,t_comparator_0>;
t_ind_0 ind_0;
using iterator = t_ind_0::iterator;
struct context {
t_ind_0::operation_hints hints_0_lower;
t_ind_0::operation_hints hints_0_upper;
};
context createContext() { return context(); }
bool insert(const t_tuple& t) {
context h;
return insert(t, h);
}
bool insert(const t_tuple& t, context& h) {
if (ind_0.insert(t, h.hints_0_lower)) {
return true;
} else return false;
}
bool insert(const RamDomain* ramDomain) {
RamDomain data[2];
std::copy(ramDomain, ramDomain + 2, data);
const t_tuple& tuple = reinterpret_cast<const t_tuple&>(data);
context h;
return insert(tuple, h);
}
bool insert(RamDomain a0,RamDomain a1) {
RamDomain data[2] = {a0,a1};
return insert(data);
}
bool contains(const t_tuple& t, context& h) const {
return ind_0.contains(t, h.hints_0_lower);
}
bool contains(const t_tuple& t) const {
context h;
return contains(t, h);
}
std::size_t size() const {
return ind_0.size();
}
iterator find(const t_tuple& t, context& h) const {
return ind_0.find(t, h.hints_0_lower);
}
iterator find(const t_tuple& t) const {
context h;
return find(t, h);
}
range<iterator> lowerUpperRange_00(const t_tuple& /* lower */, const t_tuple& /* upper */, context& /* h */) const {
return range<iterator>(ind_0.begin(),ind_0.end());
}
range<iterator> lowerUpperRange_00(const t_tuple& /* lower */, const t_tuple& /* upper */) const {
return range<iterator>(ind_0.begin(),ind_0.end());
}
range<t_ind_0::iterator> lowerUpperRange_11(const t_tuple& lower, const t_tuple& upper, context& h) const {
t_comparator_0 comparator;
int cmp = comparator(lower, upper);
if (cmp == 0) {
    auto pos = ind_0.find(lower, h.hints_0_lower);
    auto fin = ind_0.end();
    if (pos != fin) {fin = pos; ++fin;}
    return make_range(pos, fin);
}
if (cmp > 0) {
    return make_range(ind_0.end(), ind_0.end());
}
return make_range(ind_0.lower_bound(lower, h.hints_0_lower), ind_0.upper_bound(upper, h.hints_0_upper));
}
range<t_ind_0::iterator> lowerUpperRange_11(const t_tuple& lower, const t_tuple& upper) const {
context h;
return lowerUpperRange_11(lower,upper,h);
}
range<t_ind_0::iterator> lowerUpperRange_10(const t_tuple& lower, const t_tuple& upper, context& h) const {
t_comparator_0 comparator;
int cmp = comparator(lower, upper);
if (cmp > 0) {
    return make_range(ind_0.end(), ind_0.end());
}
return make_range(ind_0.lower_bound(lower, h.hints_0_lower), ind_0.upper_bound(upper, h.hints_0_upper));
}
range<t_ind_0::iterator> lowerUpperRange_10(const t_tuple& lower, const t_tuple& upper) const {
context h;
return lowerUpperRange_10(lower,upper,h);
}
bool empty() const {
return ind_0.empty();
}
std::vector<range<iterator>> partition() const {
return ind_0.getChunks(400);
}
void purge() {
ind_0.clear();
}
iterator begin() const {
return ind_0.begin();
}
iterator end() const {
return ind_0.end();
}
void printStatistics(std::ostream& o) const {
o << " arity 2 direct b-tree index 0 lex-order [0,1]\n";
ind_0.printStats(o);
}
};
struct t_btree_iiii__0_1_2_3__1000__1111 {
static constexpr Relation::arity_type Arity = 4;
using t_tuple = Tuple<RamDomain, 4>;
struct t_comparator_0{
 int operator()(const t_tuple& a, const t_tuple& b) const {
  return (ramBitCast<RamSigned>(a[0]) < ramBitCast<RamSigned>(b[0])) ? -1 : (ramBitCast<RamSigned>(a[0]) > ramBitCast<RamSigned>(b[0])) ? 1 :((ramBitCast<RamSigned>(a[1]) < ramBitCast<RamSigned>(b[1])) ? -1 : (ramBitCast<RamSigned>(a[1]) > ramBitCast<RamSigned>(b[1])) ? 1 :((ramBitCast<RamSigned>(a[2]) < ramBitCast<RamSigned>(b[2])) ? -1 : (ramBitCast<RamSigned>(a[2]) > ramBitCast<RamSigned>(b[2])) ? 1 :((ramBitCast<RamSigned>(a[3]) < ramBitCast<RamSigned>(b[3])) ? -1 : (ramBitCast<RamSigned>(a[3]) > ramBitCast<RamSigned>(b[3])) ? 1 :(0))));
 }
bool less(const t_tuple& a, const t_tuple& b) const {
  return (ramBitCast<RamSigned>(a[0]) < ramBitCast<RamSigned>(b[0]))|| (ramBitCast<RamSigned>(a[0]) == ramBitCast<RamSigned>(b[0])) && ((ramBitCast<RamSigned>(a[1]) < ramBitCast<RamSigned>(b[1]))|| (ramBitCast<RamSigned>(a[1]) == ramBitCast<RamSigned>(b[1])) && ((ramBitCast<RamSigned>(a[2]) < ramBitCast<RamSigned>(b[2]))|| (ramBitCast<RamSigned>(a[2]) == ramBitCast<RamSigned>(b[2])) && ((ramBitCast<RamSigned>(a[3]) < ramBitCast<RamSigned>(b[3])))));
 }
bool equal(const t_tuple& a, const t_tuple& b) const {
return (ramBitCast<RamSigned>(a[0]) == ramBitCast<RamSigned>(b[0]))&&(ramBitCast<RamSigned>(a[1]) == ramBitCast<RamSigned>(b[1]))&&(ramBitCast<RamSigned>(a[2]) == ramBitCast<RamSigned>(b[2]))&&(ramBitCast<RamSigned>(a[3]) == ramBitCast<RamSigned>(b[3]));
 }
};
using t_ind_0 = btree_set<t_tuple,t_comparator_0>;
t_ind_0 ind_0;
using iterator = t_ind_0::iterator;
struct context {
t_ind_0::operation_hints hints_0_lower;
t_ind_0::operation_hints hints_0_upper;
};
context createContext() { return context(); }
bool insert(const t_tuple& t) {
context h;
return insert(t, h);
}
bool insert(const t_tuple& t, context& h) {
if (ind_0.insert(t, h.hints_0_lower)) {
return true;
} else return false;
}
bool insert(const RamDomain* ramDomain) {
RamDomain data[4];
std::copy(ramDomain, ramDomain + 4, data);
const t_tuple& tuple = reinterpret_cast<const t_tuple&>(data);
context h;
return insert(tuple, h);
}
bool insert(RamDomain a0,RamDomain a1,RamDomain a2,RamDomain a3) {
RamDomain data[4] = {a0,a1,a2,a3};
return insert(data);
}
bool contains(const t_tuple& t, context& h) const {
return ind_0.contains(t, h.hints_0_lower);
}
bool contains(const t_tuple& t) const {
context h;
return contains(t, h);
}
std::size_t size() const {
return ind_0.size();
}
iterator find(const t_tuple& t, context& h) const {
return ind_0.find(t, h.hints_0_lower);
}
iterator find(const t_tuple& t) const {
context h;
return find(t, h);
}
range<iterator> lowerUpperRange_0000(const t_tuple& /* lower */, const t_tuple& /* upper */, context& /* h */) const {
return range<iterator>(ind_0.begin(),ind_0.end());
}
range<iterator> lowerUpperRange_0000(const t_tuple& /* lower */, const t_tuple& /* upper */) const {
return range<iterator>(ind_0.begin(),ind_0.end());
}
range<t_ind_0::iterator> lowerUpperRange_1000(const t_tuple& lower, const t_tuple& upper, context& h) const {
t_comparator_0 comparator;
int cmp = comparator(lower, upper);
if (cmp > 0) {
    return make_range(ind_0.end(), ind_0.end());
}
return make_range(ind_0.lower_bound(lower, h.hints_0_lower), ind_0.upper_bound(upper, h.hints_0_upper));
}
range<t_ind_0::iterator> lowerUpperRange_1000(const t_tuple& lower, const t_tuple& upper) const {
context h;
return lowerUpperRange_1000(lower,upper,h);
}
range<t_ind_0::iterator> lowerUpperRange_1111(const t_tuple& lower, const t_tuple& upper, context& h) const {
t_comparator_0 comparator;
int cmp = comparator(lower, upper);
if (cmp == 0) {
    auto pos = ind_0.find(lower, h.hints_0_lower);
    auto fin = ind_0.end();
    if (pos != fin) {fin = pos; ++fin;}
    return make_range(pos, fin);
}
if (cmp > 0) {
    return make_range(ind_0.end(), ind_0.end());
}
return make_range(ind_0.lower_bound(lower, h.hints_0_lower), ind_0.upper_bound(upper, h.hints_0_upper));
}
range<t_ind_0::iterator> lowerUpperRange_1111(const t_tuple& lower, const t_tuple& upper) const {
context h;
return lowerUpperRange_1111(lower,upper,h);
}
bool empty() const {
return ind_0.empty();
}
std::vector<range<iterator>> partition() const {
return ind_0.getChunks(400);
}
void purge() {
ind_0.clear();
}
iterator begin() const {
return ind_0.begin();
}
iterator end() const {
return ind_0.end();
}
void printStatistics(std::ostream& o) const {
o << " arity 4 direct b-tree index 0 lex-order [0,1,2,3]\n";
ind_0.printStats(o);
}
};
struct t_btree_ii__0_1__11 {
static constexpr Relation::arity_type Arity = 2;
using t_tuple = Tuple<RamDomain, 2>;
struct t_comparator_0{
 int operator()(const t_tuple& a, const t_tuple& b) const {
  return (ramBitCast<RamSigned>(a[0]) < ramBitCast<RamSigned>(b[0])) ? -1 : (ramBitCast<RamSigned>(a[0]) > ramBitCast<RamSigned>(b[0])) ? 1 :((ramBitCast<RamSigned>(a[1]) < ramBitCast<RamSigned>(b[1])) ? -1 : (ramBitCast<RamSigned>(a[1]) > ramBitCast<RamSigned>(b[1])) ? 1 :(0));
 }
bool less(const t_tuple& a, const t_tuple& b) const {
  return (ramBitCast<RamSigned>(a[0]) < ramBitCast<RamSigned>(b[0]))|| (ramBitCast<RamSigned>(a[0]) == ramBitCast<RamSigned>(b[0])) && ((ramBitCast<RamSigned>(a[1]) < ramBitCast<RamSigned>(b[1])));
 }
bool equal(const t_tuple& a, const t_tuple& b) const {
return (ramBitCast<RamSigned>(a[0]) == ramBitCast<RamSigned>(b[0]))&&(ramBitCast<RamSigned>(a[1]) == ramBitCast<RamSigned>(b[1]));
 }
};
using t_ind_0 = btree_set<t_tuple,t_comparator_0>;
t_ind_0 ind_0;
using iterator = t_ind_0::iterator;
struct context {
t_ind_0::operation_hints hints_0_lower;
t_ind_0::operation_hints hints_0_upper;
};
context createContext() { return context(); }
bool insert(const t_tuple& t) {
context h;
return insert(t, h);
}
bool insert(const t_tuple& t, context& h) {
if (ind_0.insert(t, h.hints_0_lower)) {
return true;
} else return false;
}
bool insert(const RamDomain* ramDomain) {
RamDomain data[2];
std::copy(ramDomain, ramDomain + 2, data);
const t_tuple& tuple = reinterpret_cast<const t_tuple&>(data);
context h;
return insert(tuple, h);
}
bool insert(RamDomain a0,RamDomain a1) {
RamDomain data[2] = {a0,a1};
return insert(data);
}
bool contains(const t_tuple& t, context& h) const {
return ind_0.contains(t, h.hints_0_lower);
}
bool contains(const t_tuple& t) const {
context h;
return contains(t, h);
}
std::size_t size() const {
return ind_0.size();
}
iterator find(const t_tuple& t, context& h) const {
return ind_0.find(t, h.hints_0_lower);
}
iterator find(const t_tuple& t) const {
context h;
return find(t, h);
}
range<iterator> lowerUpperRange_00(const t_tuple& /* lower */, const t_tuple& /* upper */, context& /* h */) const {
return range<iterator>(ind_0.begin(),ind_0.end());
}
range<iterator> lowerUpperRange_00(const t_tuple& /* lower */, const t_tuple& /* upper */) const {
return range<iterator>(ind_0.begin(),ind_0.end());
}
range<t_ind_0::iterator> lowerUpperRange_11(const t_tuple& lower, const t_tuple& upper, context& h) const {
t_comparator_0 comparator;
int cmp = comparator(lower, upper);
if (cmp == 0) {
    auto pos = ind_0.find(lower, h.hints_0_lower);
    auto fin = ind_0.end();
    if (pos != fin) {fin = pos; ++fin;}
    return make_range(pos, fin);
}
if (cmp > 0) {
    return make_range(ind_0.end(), ind_0.end());
}
return make_range(ind_0.lower_bound(lower, h.hints_0_lower), ind_0.upper_bound(upper, h.hints_0_upper));
}
range<t_ind_0::iterator> lowerUpperRange_11(const t_tuple& lower, const t_tuple& upper) const {
context h;
return lowerUpperRange_11(lower,upper,h);
}
bool empty() const {
return ind_0.empty();
}
std::vector<range<iterator>> partition() const {
return ind_0.getChunks(400);
}
void purge() {
ind_0.clear();
}
iterator begin() const {
return ind_0.begin();
}
iterator end() const {
return ind_0.end();
}
void printStatistics(std::ostream& o) const {
o << " arity 2 direct b-tree index 0 lex-order [0,1]\n";
ind_0.printStats(o);
}
};
struct t_btree_ii__1_0__0__11__10__01 {
static constexpr Relation::arity_type Arity = 2;
using t_tuple = Tuple<RamDomain, 2>;
struct t_comparator_0{
 int operator()(const t_tuple& a, const t_tuple& b) const {
  return (ramBitCast<RamSigned>(a[1]) < ramBitCast<RamSigned>(b[1])) ? -1 : (ramBitCast<RamSigned>(a[1]) > ramBitCast<RamSigned>(b[1])) ? 1 :((ramBitCast<RamSigned>(a[0]) < ramBitCast<RamSigned>(b[0])) ? -1 : (ramBitCast<RamSigned>(a[0]) > ramBitCast<RamSigned>(b[0])) ? 1 :(0));
 }
bool less(const t_tuple& a, const t_tuple& b) const {
  return (ramBitCast<RamSigned>(a[1]) < ramBitCast<RamSigned>(b[1]))|| (ramBitCast<RamSigned>(a[1]) == ramBitCast<RamSigned>(b[1])) && ((ramBitCast<RamSigned>(a[0]) < ramBitCast<RamSigned>(b[0])));
 }
bool equal(const t_tuple& a, const t_tuple& b) const {
return (ramBitCast<RamSigned>(a[1]) == ramBitCast<RamSigned>(b[1]))&&(ramBitCast<RamSigned>(a[0]) == ramBitCast<RamSigned>(b[0]));
 }
};
using t_ind_0 = btree_set<t_tuple,t_comparator_0>;
t_ind_0 ind_0;
struct t_comparator_1{
 int operator()(const t_tuple& a, const t_tuple& b) const {
  return (ramBitCast<RamSigned>(a[0]) < ramBitCast<RamSigned>(b[0])) ? -1 : (ramBitCast<RamSigned>(a[0]) > ramBitCast<RamSigned>(b[0])) ? 1 :(0);
 }
bool less(const t_tuple& a, const t_tuple& b) const {
  return (ramBitCast<RamSigned>(a[0]) < ramBitCast<RamSigned>(b[0]));
 }
bool equal(const t_tuple& a, const t_tuple& b) const {
return (ramBitCast<RamSigned>(a[0]) == ramBitCast<RamSigned>(b[0]));
 }
};
using t_ind_1 = btree_multiset<t_tuple,t_comparator_1>;
t_ind_1 ind_1;
using iterator = t_ind_0::iterator;
struct context {
t_ind_0::operation_hints hints_0_lower;
t_ind_0::operation_hints hints_0_upper;
t_ind_1::operation_hints hints_1_lower;
t_ind_1::operation_hints hints_1_upper;
};
context createContext() { return context(); }
bool insert(const t_tuple& t) {
context h;
return insert(t, h);
}
bool insert(const t_tuple& t, context& h) {
if (ind_0.insert(t, h.hints_0_lower)) {
ind_1.insert(t, h.hints_1_lower);
return true;
} else return false;
}
bool insert(const RamDomain* ramDomain) {
RamDomain data[2];
std::copy(ramDomain, ramDomain + 2, data);
const t_tuple& tuple = reinterpret_cast<const t_tuple&>(data);
context h;
return insert(tuple, h);
}
bool insert(RamDomain a0,RamDomain a1) {
RamDomain data[2] = {a0,a1};
return insert(data);
}
bool contains(const t_tuple& t, context& h) const {
return ind_0.contains(t, h.hints_0_lower);
}
bool contains(const t_tuple& t) const {
context h;
return contains(t, h);
}
std::size_t size() const {
return ind_0.size();
}
iterator find(const t_tuple& t, context& h) const {
return ind_0.find(t, h.hints_0_lower);
}
iterator find(const t_tuple& t) const {
context h;
return find(t, h);
}
range<iterator> lowerUpperRange_00(const t_tuple& /* lower */, const t_tuple& /* upper */, context& /* h */) const {
return range<iterator>(ind_0.begin(),ind_0.end());
}
range<iterator> lowerUpperRange_00(const t_tuple& /* lower */, const t_tuple& /* upper */) const {
return range<iterator>(ind_0.begin(),ind_0.end());
}
range<t_ind_0::iterator> lowerUpperRange_11(const t_tuple& lower, const t_tuple& upper, context& h) const {
t_comparator_0 comparator;
int cmp = comparator(lower, upper);
if (cmp == 0) {
    auto pos = ind_0.find(lower, h.hints_0_lower);
    auto fin = ind_0.end();
    if (pos != fin) {fin = pos; ++fin;}
    return make_range(pos, fin);
}
if (cmp > 0) {
    return make_range(ind_0.end(), ind_0.end());
}
return make_range(ind_0.lower_bound(lower, h.hints_0_lower), ind_0.upper_bound(upper, h.hints_0_upper));
}
range<t_ind_0::iterator> lowerUpperRange_11(const t_tuple& lower, const t_tuple& upper) const {
context h;
return lowerUpperRange_11(lower,upper,h);
}
range<t_ind_1::iterator> lowerUpperRange_10(const t_tuple& lower, const t_tuple& upper, context& h) const {
t_comparator_1 comparator;
int cmp = comparator(lower, upper);
if (cmp > 0) {
    return make_range(ind_1.end(), ind_1.end());
}
return make_range(ind_1.lower_bound(lower, h.hints_1_lower), ind_1.upper_bound(upper, h.hints_1_upper));
}
range<t_ind_1::iterator> lowerUpperRange_10(const t_tuple& lower, const t_tuple& upper) const {
context h;
return lowerUpperRange_10(lower,upper,h);
}
range<t_ind_0::iterator> lowerUpperRange_01(const t_tuple& lower, const t_tuple& upper, context& h) const {
t_comparator_0 comparator;
int cmp = comparator(lower, upper);
if (cmp > 0) {
    return make_range(ind_0.end(), ind_0.end());
}
return make_range(ind_0.lower_bound(lower, h.hints_0_lower), ind_0.upper_bound(upper, h.hints_0_upper));
}
range<t_ind_0::iterator> lowerUpperRange_01(const t_tuple& lower, const t_tuple& upper) const {
context h;
return lowerUpperRange_01(lower,upper,h);
}
bool empty() const {
return ind_0.empty();
}
std::vector<range<iterator>> partition() const {
return ind_0.getChunks(400);
}
void purge() {
ind_0.clear();
ind_1.clear();
}
iterator begin() const {
return ind_0.begin();
}
iterator end() const {
return ind_0.end();
}
void printStatistics(std::ostream& o) const {
o << " arity 2 direct b-tree index 0 lex-order [1,0]\n";
ind_0.printStats(o);
o << " arity 2 direct b-tree index 1 lex-order [0]\n";
ind_1.printStats(o);
}
};
struct t_btree_iii__0_1_2__100__120__111 {
static constexpr Relation::arity_type Arity = 3;
using t_tuple = Tuple<RamDomain, 3>;
struct t_comparator_0{
 int operator()(const t_tuple& a, const t_tuple& b) const {
  return (ramBitCast<RamSigned>(a[0]) < ramBitCast<RamSigned>(b[0])) ? -1 : (ramBitCast<RamSigned>(a[0]) > ramBitCast<RamSigned>(b[0])) ? 1 :((ramBitCast<RamSigned>(a[1]) < ramBitCast<RamSigned>(b[1])) ? -1 : (ramBitCast<RamSigned>(a[1]) > ramBitCast<RamSigned>(b[1])) ? 1 :((ramBitCast<RamSigned>(a[2]) < ramBitCast<RamSigned>(b[2])) ? -1 : (ramBitCast<RamSigned>(a[2]) > ramBitCast<RamSigned>(b[2])) ? 1 :(0)));
 }
bool less(const t_tuple& a, const t_tuple& b) const {
  return (ramBitCast<RamSigned>(a[0]) < ramBitCast<RamSigned>(b[0]))|| (ramBitCast<RamSigned>(a[0]) == ramBitCast<RamSigned>(b[0])) && ((ramBitCast<RamSigned>(a[1]) < ramBitCast<RamSigned>(b[1]))|| (ramBitCast<RamSigned>(a[1]) == ramBitCast<RamSigned>(b[1])) && ((ramBitCast<RamSigned>(a[2]) < ramBitCast<RamSigned>(b[2]))));
 }
bool equal(const t_tuple& a, const t_tuple& b) const {
return (ramBitCast<RamSigned>(a[0]) == ramBitCast<RamSigned>(b[0]))&&(ramBitCast<RamSigned>(a[1]) == ramBitCast<RamSigned>(b[1]))&&(ramBitCast<RamSigned>(a[2]) == ramBitCast<RamSigned>(b[2]));
 }
};
using t_ind_0 = btree_set<t_tuple,t_comparator_0>;
t_ind_0 ind_0;
using iterator = t_ind_0::iterator;
struct context {
t_ind_0::operation_hints hints_0_lower;
t_ind_0::operation_hints hints_0_upper;
};
context createContext() { return context(); }
bool insert(const t_tuple& t) {
context h;
return insert(t, h);
}
bool insert(const t_tuple& t, context& h) {
if (ind_0.insert(t, h.hints_0_lower)) {
return true;
} else return false;
}
bool insert(const RamDomain* ramDomain) {
RamDomain data[3];
std::copy(ramDomain, ramDomain + 3, data);
const t_tuple& tuple = reinterpret_cast<const t_tuple&>(data);
context h;
return insert(tuple, h);
}
bool insert(RamDomain a0,RamDomain a1,RamDomain a2) {
RamDomain data[3] = {a0,a1,a2};
return insert(data);
}
bool contains(const t_tuple& t, context& h) const {
return ind_0.contains(t, h.hints_0_lower);
}
bool contains(const t_tuple& t) const {
context h;
return contains(t, h);
}
std::size_t size() const {
return ind_0.size();
}
iterator find(const t_tuple& t, context& h) const {
return ind_0.find(t, h.hints_0_lower);
}
iterator find(const t_tuple& t) const {
context h;
return find(t, h);
}
range<iterator> lowerUpperRange_000(const t_tuple& /* lower */, const t_tuple& /* upper */, context& /* h */) const {
return range<iterator>(ind_0.begin(),ind_0.end());
}
range<iterator> lowerUpperRange_000(const t_tuple& /* lower */, const t_tuple& /* upper */) const {
return range<iterator>(ind_0.begin(),ind_0.end());
}
range<t_ind_0::iterator> lowerUpperRange_100(const t_tuple& lower, const t_tuple& upper, context& h) const {
t_comparator_0 comparator;
int cmp = comparator(lower, upper);
if (cmp > 0) {
    return make_range(ind_0.end(), ind_0.end());
}
return make_range(ind_0.lower_bound(lower, h.hints_0_lower), ind_0.upper_bound(upper, h.hints_0_upper));
}
range<t_ind_0::iterator> lowerUpperRange_100(const t_tuple& lower, const t_tuple& upper) const {
context h;
return lowerUpperRange_100(lower,upper,h);
}
range<t_ind_0::iterator> lowerUpperRange_120(const t_tuple& lower, const t_tuple& upper, context& h) const {
t_comparator_0 comparator;
int cmp = comparator(lower, upper);
if (cmp > 0) {
    return make_range(ind_0.end(), ind_0.end());
}
return make_range(ind_0.lower_bound(lower, h.hints_0_lower), ind_0.upper_bound(upper, h.hints_0_upper));
}
range<t_ind_0::iterator> lowerUpperRange_120(const t_tuple& lower, const t_tuple& upper) const {
context h;
return lowerUpperRange_120(lower,upper,h);
}
range<t_ind_0::iterator> lowerUpperRange_111(const t_tuple& lower, const t_tuple& upper, context& h) const {
t_comparator_0 comparator;
int cmp = comparator(lower, upper);
if (cmp == 0) {
    auto pos = ind_0.find(lower, h.hints_0_lower);
    auto fin = ind_0.end();
    if (pos != fin) {fin = pos; ++fin;}
    return make_range(pos, fin);
}
if (cmp > 0) {
    return make_range(ind_0.end(), ind_0.end());
}
return make_range(ind_0.lower_bound(lower, h.hints_0_lower), ind_0.upper_bound(upper, h.hints_0_upper));
}
range<t_ind_0::iterator> lowerUpperRange_111(const t_tuple& lower, const t_tuple& upper) const {
context h;
return lowerUpperRange_111(lower,upper,h);
}
bool empty() const {
return ind_0.empty();
}
std::vector<range<iterator>> partition() const {
return ind_0.getChunks(400);
}
void purge() {
ind_0.clear();
}
iterator begin() const {
return ind_0.begin();
}
iterator end() const {
return ind_0.end();
}
void printStatistics(std::ostream& o) const {
o << " arity 3 direct b-tree index 0 lex-order [0,1,2]\n";
ind_0.printStats(o);
}
};
struct t_btree_iii__0_1_2__111 {
static constexpr Relation::arity_type Arity = 3;
using t_tuple = Tuple<RamDomain, 3>;
struct t_comparator_0{
 int operator()(const t_tuple& a, const t_tuple& b) const {
  return (ramBitCast<RamSigned>(a[0]) < ramBitCast<RamSigned>(b[0])) ? -1 : (ramBitCast<RamSigned>(a[0]) > ramBitCast<RamSigned>(b[0])) ? 1 :((ramBitCast<RamSigned>(a[1]) < ramBitCast<RamSigned>(b[1])) ? -1 : (ramBitCast<RamSigned>(a[1]) > ramBitCast<RamSigned>(b[1])) ? 1 :((ramBitCast<RamSigned>(a[2]) < ramBitCast<RamSigned>(b[2])) ? -1 : (ramBitCast<RamSigned>(a[2]) > ramBitCast<RamSigned>(b[2])) ? 1 :(0)));
 }
bool less(const t_tuple& a, const t_tuple& b) const {
  return (ramBitCast<RamSigned>(a[0]) < ramBitCast<RamSigned>(b[0]))|| (ramBitCast<RamSigned>(a[0]) == ramBitCast<RamSigned>(b[0])) && ((ramBitCast<RamSigned>(a[1]) < ramBitCast<RamSigned>(b[1]))|| (ramBitCast<RamSigned>(a[1]) == ramBitCast<RamSigned>(b[1])) && ((ramBitCast<RamSigned>(a[2]) < ramBitCast<RamSigned>(b[2]))));
 }
bool equal(const t_tuple& a, const t_tuple& b) const {
return (ramBitCast<RamSigned>(a[0]) == ramBitCast<RamSigned>(b[0]))&&(ramBitCast<RamSigned>(a[1]) == ramBitCast<RamSigned>(b[1]))&&(ramBitCast<RamSigned>(a[2]) == ramBitCast<RamSigned>(b[2]));
 }
};
using t_ind_0 = btree_set<t_tuple,t_comparator_0>;
t_ind_0 ind_0;
using iterator = t_ind_0::iterator;
struct context {
t_ind_0::operation_hints hints_0_lower;
t_ind_0::operation_hints hints_0_upper;
};
context createContext() { return context(); }
bool insert(const t_tuple& t) {
context h;
return insert(t, h);
}
bool insert(const t_tuple& t, context& h) {
if (ind_0.insert(t, h.hints_0_lower)) {
return true;
} else return false;
}
bool insert(const RamDomain* ramDomain) {
RamDomain data[3];
std::copy(ramDomain, ramDomain + 3, data);
const t_tuple& tuple = reinterpret_cast<const t_tuple&>(data);
context h;
return insert(tuple, h);
}
bool insert(RamDomain a0,RamDomain a1,RamDomain a2) {
RamDomain data[3] = {a0,a1,a2};
return insert(data);
}
bool contains(const t_tuple& t, context& h) const {
return ind_0.contains(t, h.hints_0_lower);
}
bool contains(const t_tuple& t) const {
context h;
return contains(t, h);
}
std::size_t size() const {
return ind_0.size();
}
iterator find(const t_tuple& t, context& h) const {
return ind_0.find(t, h.hints_0_lower);
}
iterator find(const t_tuple& t) const {
context h;
return find(t, h);
}
range<iterator> lowerUpperRange_000(const t_tuple& /* lower */, const t_tuple& /* upper */, context& /* h */) const {
return range<iterator>(ind_0.begin(),ind_0.end());
}
range<iterator> lowerUpperRange_000(const t_tuple& /* lower */, const t_tuple& /* upper */) const {
return range<iterator>(ind_0.begin(),ind_0.end());
}
range<t_ind_0::iterator> lowerUpperRange_111(const t_tuple& lower, const t_tuple& upper, context& h) const {
t_comparator_0 comparator;
int cmp = comparator(lower, upper);
if (cmp == 0) {
    auto pos = ind_0.find(lower, h.hints_0_lower);
    auto fin = ind_0.end();
    if (pos != fin) {fin = pos; ++fin;}
    return make_range(pos, fin);
}
if (cmp > 0) {
    return make_range(ind_0.end(), ind_0.end());
}
return make_range(ind_0.lower_bound(lower, h.hints_0_lower), ind_0.upper_bound(upper, h.hints_0_upper));
}
range<t_ind_0::iterator> lowerUpperRange_111(const t_tuple& lower, const t_tuple& upper) const {
context h;
return lowerUpperRange_111(lower,upper,h);
}
bool empty() const {
return ind_0.empty();
}
std::vector<range<iterator>> partition() const {
return ind_0.getChunks(400);
}
void purge() {
ind_0.clear();
}
iterator begin() const {
return ind_0.begin();
}
iterator end() const {
return ind_0.end();
}
void printStatistics(std::ostream& o) const {
o << " arity 3 direct b-tree index 0 lex-order [0,1,2]\n";
ind_0.printStats(o);
}
};
struct t_btree_i__0__1 {
static constexpr Relation::arity_type Arity = 1;
using t_tuple = Tuple<RamDomain, 1>;
struct t_comparator_0{
 int operator()(const t_tuple& a, const t_tuple& b) const {
  return (ramBitCast<RamSigned>(a[0]) < ramBitCast<RamSigned>(b[0])) ? -1 : (ramBitCast<RamSigned>(a[0]) > ramBitCast<RamSigned>(b[0])) ? 1 :(0);
 }
bool less(const t_tuple& a, const t_tuple& b) const {
  return (ramBitCast<RamSigned>(a[0]) < ramBitCast<RamSigned>(b[0]));
 }
bool equal(const t_tuple& a, const t_tuple& b) const {
return (ramBitCast<RamSigned>(a[0]) == ramBitCast<RamSigned>(b[0]));
 }
};
using t_ind_0 = btree_set<t_tuple,t_comparator_0>;
t_ind_0 ind_0;
using iterator = t_ind_0::iterator;
struct context {
t_ind_0::operation_hints hints_0_lower;
t_ind_0::operation_hints hints_0_upper;
};
context createContext() { return context(); }
bool insert(const t_tuple& t) {
context h;
return insert(t, h);
}
bool insert(const t_tuple& t, context& h) {
if (ind_0.insert(t, h.hints_0_lower)) {
return true;
} else return false;
}
bool insert(const RamDomain* ramDomain) {
RamDomain data[1];
std::copy(ramDomain, ramDomain + 1, data);
const t_tuple& tuple = reinterpret_cast<const t_tuple&>(data);
context h;
return insert(tuple, h);
}
bool insert(RamDomain a0) {
RamDomain data[1] = {a0};
return insert(data);
}
bool contains(const t_tuple& t, context& h) const {
return ind_0.contains(t, h.hints_0_lower);
}
bool contains(const t_tuple& t) const {
context h;
return contains(t, h);
}
std::size_t size() const {
return ind_0.size();
}
iterator find(const t_tuple& t, context& h) const {
return ind_0.find(t, h.hints_0_lower);
}
iterator find(const t_tuple& t) const {
context h;
return find(t, h);
}
range<iterator> lowerUpperRange_0(const t_tuple& /* lower */, const t_tuple& /* upper */, context& /* h */) const {
return range<iterator>(ind_0.begin(),ind_0.end());
}
range<iterator> lowerUpperRange_0(const t_tuple& /* lower */, const t_tuple& /* upper */) const {
return range<iterator>(ind_0.begin(),ind_0.end());
}
range<t_ind_0::iterator> lowerUpperRange_1(const t_tuple& lower, const t_tuple& upper, context& h) const {
t_comparator_0 comparator;
int cmp = comparator(lower, upper);
if (cmp == 0) {
    auto pos = ind_0.find(lower, h.hints_0_lower);
    auto fin = ind_0.end();
    if (pos != fin) {fin = pos; ++fin;}
    return make_range(pos, fin);
}
if (cmp > 0) {
    return make_range(ind_0.end(), ind_0.end());
}
return make_range(ind_0.lower_bound(lower, h.hints_0_lower), ind_0.upper_bound(upper, h.hints_0_upper));
}
range<t_ind_0::iterator> lowerUpperRange_1(const t_tuple& lower, const t_tuple& upper) const {
context h;
return lowerUpperRange_1(lower,upper,h);
}
bool empty() const {
return ind_0.empty();
}
std::vector<range<iterator>> partition() const {
return ind_0.getChunks(400);
}
void purge() {
ind_0.clear();
}
iterator begin() const {
return ind_0.begin();
}
iterator end() const {
return ind_0.end();
}
void printStatistics(std::ostream& o) const {
o << " arity 1 direct b-tree index 0 lex-order [0]\n";
ind_0.printStats(o);
}
};
struct t_btree_ii__0_1__11__12 {
static constexpr Relation::arity_type Arity = 2;
using t_tuple = Tuple<RamDomain, 2>;
struct t_comparator_0{
 int operator()(const t_tuple& a, const t_tuple& b) const {
  return (ramBitCast<RamSigned>(a[0]) < ramBitCast<RamSigned>(b[0])) ? -1 : (ramBitCast<RamSigned>(a[0]) > ramBitCast<RamSigned>(b[0])) ? 1 :((ramBitCast<RamSigned>(a[1]) < ramBitCast<RamSigned>(b[1])) ? -1 : (ramBitCast<RamSigned>(a[1]) > ramBitCast<RamSigned>(b[1])) ? 1 :(0));
 }
bool less(const t_tuple& a, const t_tuple& b) const {
  return (ramBitCast<RamSigned>(a[0]) < ramBitCast<RamSigned>(b[0]))|| (ramBitCast<RamSigned>(a[0]) == ramBitCast<RamSigned>(b[0])) && ((ramBitCast<RamSigned>(a[1]) < ramBitCast<RamSigned>(b[1])));
 }
bool equal(const t_tuple& a, const t_tuple& b) const {
return (ramBitCast<RamSigned>(a[0]) == ramBitCast<RamSigned>(b[0]))&&(ramBitCast<RamSigned>(a[1]) == ramBitCast<RamSigned>(b[1]));
 }
};
using t_ind_0 = btree_set<t_tuple,t_comparator_0>;
t_ind_0 ind_0;
using iterator = t_ind_0::iterator;
struct context {
t_ind_0::operation_hints hints_0_lower;
t_ind_0::operation_hints hints_0_upper;
};
context createContext() { return context(); }
bool insert(const t_tuple& t) {
context h;
return insert(t, h);
}
bool insert(const t_tuple& t, context& h) {
if (ind_0.insert(t, h.hints_0_lower)) {
return true;
} else return false;
}
bool insert(const RamDomain* ramDomain) {
RamDomain data[2];
std::copy(ramDomain, ramDomain + 2, data);
const t_tuple& tuple = reinterpret_cast<const t_tuple&>(data);
context h;
return insert(tuple, h);
}
bool insert(RamDomain a0,RamDomain a1) {
RamDomain data[2] = {a0,a1};
return insert(data);
}
bool contains(const t_tuple& t, context& h) const {
return ind_0.contains(t, h.hints_0_lower);
}
bool contains(const t_tuple& t) const {
context h;
return contains(t, h);
}
std::size_t size() const {
return ind_0.size();
}
iterator find(const t_tuple& t, context& h) const {
return ind_0.find(t, h.hints_0_lower);
}
iterator find(const t_tuple& t) const {
context h;
return find(t, h);
}
range<iterator> lowerUpperRange_00(const t_tuple& /* lower */, const t_tuple& /* upper */, context& /* h */) const {
return range<iterator>(ind_0.begin(),ind_0.end());
}
range<iterator> lowerUpperRange_00(const t_tuple& /* lower */, const t_tuple& /* upper */) const {
return range<iterator>(ind_0.begin(),ind_0.end());
}
range<t_ind_0::iterator> lowerUpperRange_11(const t_tuple& lower, const t_tuple& upper, context& h) const {
t_comparator_0 comparator;
int cmp = comparator(lower, upper);
if (cmp == 0) {
    auto pos = ind_0.find(lower, h.hints_0_lower);
    auto fin = ind_0.end();
    if (pos != fin) {fin = pos; ++fin;}
    return make_range(pos, fin);
}
if (cmp > 0) {
    return make_range(ind_0.end(), ind_0.end());
}
return make_range(ind_0.lower_bound(lower, h.hints_0_lower), ind_0.upper_bound(upper, h.hints_0_upper));
}
range<t_ind_0::iterator> lowerUpperRange_11(const t_tuple& lower, const t_tuple& upper) const {
context h;
return lowerUpperRange_11(lower,upper,h);
}
range<t_ind_0::iterator> lowerUpperRange_12(const t_tuple& lower, const t_tuple& upper, context& h) const {
t_comparator_0 comparator;
int cmp = comparator(lower, upper);
if (cmp > 0) {
    return make_range(ind_0.end(), ind_0.end());
}
return make_range(ind_0.lower_bound(lower, h.hints_0_lower), ind_0.upper_bound(upper, h.hints_0_upper));
}
range<t_ind_0::iterator> lowerUpperRange_12(const t_tuple& lower, const t_tuple& upper) const {
context h;
return lowerUpperRange_12(lower,upper,h);
}
bool empty() const {
return ind_0.empty();
}
std::vector<range<iterator>> partition() const {
return ind_0.getChunks(400);
}
void purge() {
ind_0.clear();
}
iterator begin() const {
return ind_0.begin();
}
iterator end() const {
return ind_0.end();
}
void printStatistics(std::ostream& o) const {
o << " arity 2 direct b-tree index 0 lex-order [0,1]\n";
ind_0.printStats(o);
}
};
struct t_btree_ii__1_0__11__01 {
static constexpr Relation::arity_type Arity = 2;
using t_tuple = Tuple<RamDomain, 2>;
struct t_comparator_0{
 int operator()(const t_tuple& a, const t_tuple& b) const {
  return (ramBitCast<RamSigned>(a[1]) < ramBitCast<RamSigned>(b[1])) ? -1 : (ramBitCast<RamSigned>(a[1]) > ramBitCast<RamSigned>(b[1])) ? 1 :((ramBitCast<RamSigned>(a[0]) < ramBitCast<RamSigned>(b[0])) ? -1 : (ramBitCast<RamSigned>(a[0]) > ramBitCast<RamSigned>(b[0])) ? 1 :(0));
 }
bool less(const t_tuple& a, const t_tuple& b) const {
  return (ramBitCast<RamSigned>(a[1]) < ramBitCast<RamSigned>(b[1]))|| (ramBitCast<RamSigned>(a[1]) == ramBitCast<RamSigned>(b[1])) && ((ramBitCast<RamSigned>(a[0]) < ramBitCast<RamSigned>(b[0])));
 }
bool equal(const t_tuple& a, const t_tuple& b) const {
return (ramBitCast<RamSigned>(a[1]) == ramBitCast<RamSigned>(b[1]))&&(ramBitCast<RamSigned>(a[0]) == ramBitCast<RamSigned>(b[0]));
 }
};
using t_ind_0 = btree_set<t_tuple,t_comparator_0>;
t_ind_0 ind_0;
using iterator = t_ind_0::iterator;
struct context {
t_ind_0::operation_hints hints_0_lower;
t_ind_0::operation_hints hints_0_upper;
};
context createContext() { return context(); }
bool insert(const t_tuple& t) {
context h;
return insert(t, h);
}
bool insert(const t_tuple& t, context& h) {
if (ind_0.insert(t, h.hints_0_lower)) {
return true;
} else return false;
}
bool insert(const RamDomain* ramDomain) {
RamDomain data[2];
std::copy(ramDomain, ramDomain + 2, data);
const t_tuple& tuple = reinterpret_cast<const t_tuple&>(data);
context h;
return insert(tuple, h);
}
bool insert(RamDomain a0,RamDomain a1) {
RamDomain data[2] = {a0,a1};
return insert(data);
}
bool contains(const t_tuple& t, context& h) const {
return ind_0.contains(t, h.hints_0_lower);
}
bool contains(const t_tuple& t) const {
context h;
return contains(t, h);
}
std::size_t size() const {
return ind_0.size();
}
iterator find(const t_tuple& t, context& h) const {
return ind_0.find(t, h.hints_0_lower);
}
iterator find(const t_tuple& t) const {
context h;
return find(t, h);
}
range<iterator> lowerUpperRange_00(const t_tuple& /* lower */, const t_tuple& /* upper */, context& /* h */) const {
return range<iterator>(ind_0.begin(),ind_0.end());
}
range<iterator> lowerUpperRange_00(const t_tuple& /* lower */, const t_tuple& /* upper */) const {
return range<iterator>(ind_0.begin(),ind_0.end());
}
range<t_ind_0::iterator> lowerUpperRange_11(const t_tuple& lower, const t_tuple& upper, context& h) const {
t_comparator_0 comparator;
int cmp = comparator(lower, upper);
if (cmp == 0) {
    auto pos = ind_0.find(lower, h.hints_0_lower);
    auto fin = ind_0.end();
    if (pos != fin) {fin = pos; ++fin;}
    return make_range(pos, fin);
}
if (cmp > 0) {
    return make_range(ind_0.end(), ind_0.end());
}
return make_range(ind_0.lower_bound(lower, h.hints_0_lower), ind_0.upper_bound(upper, h.hints_0_upper));
}
range<t_ind_0::iterator> lowerUpperRange_11(const t_tuple& lower, const t_tuple& upper) const {
context h;
return lowerUpperRange_11(lower,upper,h);
}
range<t_ind_0::iterator> lowerUpperRange_01(const t_tuple& lower, const t_tuple& upper, context& h) const {
t_comparator_0 comparator;
int cmp = comparator(lower, upper);
if (cmp > 0) {
    return make_range(ind_0.end(), ind_0.end());
}
return make_range(ind_0.lower_bound(lower, h.hints_0_lower), ind_0.upper_bound(upper, h.hints_0_upper));
}
range<t_ind_0::iterator> lowerUpperRange_01(const t_tuple& lower, const t_tuple& upper) const {
context h;
return lowerUpperRange_01(lower,upper,h);
}
bool empty() const {
return ind_0.empty();
}
std::vector<range<iterator>> partition() const {
return ind_0.getChunks(400);
}
void purge() {
ind_0.clear();
}
iterator begin() const {
return ind_0.begin();
}
iterator end() const {
return ind_0.end();
}
void printStatistics(std::ostream& o) const {
o << " arity 2 direct b-tree index 0 lex-order [1,0]\n";
ind_0.printStats(o);
}
};
struct t_btree_iii__1_2_0__011__111 {
static constexpr Relation::arity_type Arity = 3;
using t_tuple = Tuple<RamDomain, 3>;
struct t_comparator_0{
 int operator()(const t_tuple& a, const t_tuple& b) const {
  return (ramBitCast<RamSigned>(a[1]) < ramBitCast<RamSigned>(b[1])) ? -1 : (ramBitCast<RamSigned>(a[1]) > ramBitCast<RamSigned>(b[1])) ? 1 :((ramBitCast<RamSigned>(a[2]) < ramBitCast<RamSigned>(b[2])) ? -1 : (ramBitCast<RamSigned>(a[2]) > ramBitCast<RamSigned>(b[2])) ? 1 :((ramBitCast<RamSigned>(a[0]) < ramBitCast<RamSigned>(b[0])) ? -1 : (ramBitCast<RamSigned>(a[0]) > ramBitCast<RamSigned>(b[0])) ? 1 :(0)));
 }
bool less(const t_tuple& a, const t_tuple& b) const {
  return (ramBitCast<RamSigned>(a[1]) < ramBitCast<RamSigned>(b[1]))|| (ramBitCast<RamSigned>(a[1]) == ramBitCast<RamSigned>(b[1])) && ((ramBitCast<RamSigned>(a[2]) < ramBitCast<RamSigned>(b[2]))|| (ramBitCast<RamSigned>(a[2]) == ramBitCast<RamSigned>(b[2])) && ((ramBitCast<RamSigned>(a[0]) < ramBitCast<RamSigned>(b[0]))));
 }
bool equal(const t_tuple& a, const t_tuple& b) const {
return (ramBitCast<RamSigned>(a[1]) == ramBitCast<RamSigned>(b[1]))&&(ramBitCast<RamSigned>(a[2]) == ramBitCast<RamSigned>(b[2]))&&(ramBitCast<RamSigned>(a[0]) == ramBitCast<RamSigned>(b[0]));
 }
};
using t_ind_0 = btree_set<t_tuple,t_comparator_0>;
t_ind_0 ind_0;
using iterator = t_ind_0::iterator;
struct context {
t_ind_0::operation_hints hints_0_lower;
t_ind_0::operation_hints hints_0_upper;
};
context createContext() { return context(); }
bool insert(const t_tuple& t) {
context h;
return insert(t, h);
}
bool insert(const t_tuple& t, context& h) {
if (ind_0.insert(t, h.hints_0_lower)) {
return true;
} else return false;
}
bool insert(const RamDomain* ramDomain) {
RamDomain data[3];
std::copy(ramDomain, ramDomain + 3, data);
const t_tuple& tuple = reinterpret_cast<const t_tuple&>(data);
context h;
return insert(tuple, h);
}
bool insert(RamDomain a0,RamDomain a1,RamDomain a2) {
RamDomain data[3] = {a0,a1,a2};
return insert(data);
}
bool contains(const t_tuple& t, context& h) const {
return ind_0.contains(t, h.hints_0_lower);
}
bool contains(const t_tuple& t) const {
context h;
return contains(t, h);
}
std::size_t size() const {
return ind_0.size();
}
iterator find(const t_tuple& t, context& h) const {
return ind_0.find(t, h.hints_0_lower);
}
iterator find(const t_tuple& t) const {
context h;
return find(t, h);
}
range<iterator> lowerUpperRange_000(const t_tuple& /* lower */, const t_tuple& /* upper */, context& /* h */) const {
return range<iterator>(ind_0.begin(),ind_0.end());
}
range<iterator> lowerUpperRange_000(const t_tuple& /* lower */, const t_tuple& /* upper */) const {
return range<iterator>(ind_0.begin(),ind_0.end());
}
range<t_ind_0::iterator> lowerUpperRange_011(const t_tuple& lower, const t_tuple& upper, context& h) const {
t_comparator_0 comparator;
int cmp = comparator(lower, upper);
if (cmp > 0) {
    return make_range(ind_0.end(), ind_0.end());
}
return make_range(ind_0.lower_bound(lower, h.hints_0_lower), ind_0.upper_bound(upper, h.hints_0_upper));
}
range<t_ind_0::iterator> lowerUpperRange_011(const t_tuple& lower, const t_tuple& upper) const {
context h;
return lowerUpperRange_011(lower,upper,h);
}
range<t_ind_0::iterator> lowerUpperRange_111(const t_tuple& lower, const t_tuple& upper, context& h) const {
t_comparator_0 comparator;
int cmp = comparator(lower, upper);
if (cmp == 0) {
    auto pos = ind_0.find(lower, h.hints_0_lower);
    auto fin = ind_0.end();
    if (pos != fin) {fin = pos; ++fin;}
    return make_range(pos, fin);
}
if (cmp > 0) {
    return make_range(ind_0.end(), ind_0.end());
}
return make_range(ind_0.lower_bound(lower, h.hints_0_lower), ind_0.upper_bound(upper, h.hints_0_upper));
}
range<t_ind_0::iterator> lowerUpperRange_111(const t_tuple& lower, const t_tuple& upper) const {
context h;
return lowerUpperRange_111(lower,upper,h);
}
bool empty() const {
return ind_0.empty();
}
std::vector<range<iterator>> partition() const {
return ind_0.getChunks(400);
}
void purge() {
ind_0.clear();
}
iterator begin() const {
return ind_0.begin();
}
iterator end() const {
return ind_0.end();
}
void printStatistics(std::ostream& o) const {
o << " arity 3 direct b-tree index 0 lex-order [1,2,0]\n";
ind_0.printStats(o);
}
};
struct t_btree_iiii__0_1_2_3__1111 {
static constexpr Relation::arity_type Arity = 4;
using t_tuple = Tuple<RamDomain, 4>;
struct t_comparator_0{
 int operator()(const t_tuple& a, const t_tuple& b) const {
  return (ramBitCast<RamSigned>(a[0]) < ramBitCast<RamSigned>(b[0])) ? -1 : (ramBitCast<RamSigned>(a[0]) > ramBitCast<RamSigned>(b[0])) ? 1 :((ramBitCast<RamSigned>(a[1]) < ramBitCast<RamSigned>(b[1])) ? -1 : (ramBitCast<RamSigned>(a[1]) > ramBitCast<RamSigned>(b[1])) ? 1 :((ramBitCast<RamSigned>(a[2]) < ramBitCast<RamSigned>(b[2])) ? -1 : (ramBitCast<RamSigned>(a[2]) > ramBitCast<RamSigned>(b[2])) ? 1 :((ramBitCast<RamSigned>(a[3]) < ramBitCast<RamSigned>(b[3])) ? -1 : (ramBitCast<RamSigned>(a[3]) > ramBitCast<RamSigned>(b[3])) ? 1 :(0))));
 }
bool less(const t_tuple& a, const t_tuple& b) const {
  return (ramBitCast<RamSigned>(a[0]) < ramBitCast<RamSigned>(b[0]))|| (ramBitCast<RamSigned>(a[0]) == ramBitCast<RamSigned>(b[0])) && ((ramBitCast<RamSigned>(a[1]) < ramBitCast<RamSigned>(b[1]))|| (ramBitCast<RamSigned>(a[1]) == ramBitCast<RamSigned>(b[1])) && ((ramBitCast<RamSigned>(a[2]) < ramBitCast<RamSigned>(b[2]))|| (ramBitCast<RamSigned>(a[2]) == ramBitCast<RamSigned>(b[2])) && ((ramBitCast<RamSigned>(a[3]) < ramBitCast<RamSigned>(b[3])))));
 }
bool equal(const t_tuple& a, const t_tuple& b) const {
return (ramBitCast<RamSigned>(a[0]) == ramBitCast<RamSigned>(b[0]))&&(ramBitCast<RamSigned>(a[1]) == ramBitCast<RamSigned>(b[1]))&&(ramBitCast<RamSigned>(a[2]) == ramBitCast<RamSigned>(b[2]))&&(ramBitCast<RamSigned>(a[3]) == ramBitCast<RamSigned>(b[3]));
 }
};
using t_ind_0 = btree_set<t_tuple,t_comparator_0>;
t_ind_0 ind_0;
using iterator = t_ind_0::iterator;
struct context {
t_ind_0::operation_hints hints_0_lower;
t_ind_0::operation_hints hints_0_upper;
};
context createContext() { return context(); }
bool insert(const t_tuple& t) {
context h;
return insert(t, h);
}
bool insert(const t_tuple& t, context& h) {
if (ind_0.insert(t, h.hints_0_lower)) {
return true;
} else return false;
}
bool insert(const RamDomain* ramDomain) {
RamDomain data[4];
std::copy(ramDomain, ramDomain + 4, data);
const t_tuple& tuple = reinterpret_cast<const t_tuple&>(data);
context h;
return insert(tuple, h);
}
bool insert(RamDomain a0,RamDomain a1,RamDomain a2,RamDomain a3) {
RamDomain data[4] = {a0,a1,a2,a3};
return insert(data);
}
bool contains(const t_tuple& t, context& h) const {
return ind_0.contains(t, h.hints_0_lower);
}
bool contains(const t_tuple& t) const {
context h;
return contains(t, h);
}
std::size_t size() const {
return ind_0.size();
}
iterator find(const t_tuple& t, context& h) const {
return ind_0.find(t, h.hints_0_lower);
}
iterator find(const t_tuple& t) const {
context h;
return find(t, h);
}
range<iterator> lowerUpperRange_0000(const t_tuple& /* lower */, const t_tuple& /* upper */, context& /* h */) const {
return range<iterator>(ind_0.begin(),ind_0.end());
}
range<iterator> lowerUpperRange_0000(const t_tuple& /* lower */, const t_tuple& /* upper */) const {
return range<iterator>(ind_0.begin(),ind_0.end());
}
range<t_ind_0::iterator> lowerUpperRange_1111(const t_tuple& lower, const t_tuple& upper, context& h) const {
t_comparator_0 comparator;
int cmp = comparator(lower, upper);
if (cmp == 0) {
    auto pos = ind_0.find(lower, h.hints_0_lower);
    auto fin = ind_0.end();
    if (pos != fin) {fin = pos; ++fin;}
    return make_range(pos, fin);
}
if (cmp > 0) {
    return make_range(ind_0.end(), ind_0.end());
}
return make_range(ind_0.lower_bound(lower, h.hints_0_lower), ind_0.upper_bound(upper, h.hints_0_upper));
}
range<t_ind_0::iterator> lowerUpperRange_1111(const t_tuple& lower, const t_tuple& upper) const {
context h;
return lowerUpperRange_1111(lower,upper,h);
}
bool empty() const {
return ind_0.empty();
}
std::vector<range<iterator>> partition() const {
return ind_0.getChunks(400);
}
void purge() {
ind_0.clear();
}
iterator begin() const {
return ind_0.begin();
}
iterator end() const {
return ind_0.end();
}
void printStatistics(std::ostream& o) const {
o << " arity 4 direct b-tree index 0 lex-order [0,1,2,3]\n";
ind_0.printStats(o);
}
};

class Sf_AvailableExpressions : public SouffleProgram {
private:
static inline bool regex_wrapper(const std::string& pattern, const std::string& text) {
   bool result = false; 
   try { result = std::regex_match(text, std::regex(pattern)); } catch(...) { 
     std::cerr << "warning: wrong pattern provided for match(\"" << pattern << "\",\"" << text << "\").\n";
}
   return result;
}
private:
static inline std::string substr_wrapper(const std::string& str, std::size_t idx, std::size_t len) {
   std::string result; 
   try { result = str.substr(idx,len); } catch(...) { 
     std::cerr << "warning: wrong index position provided by substr(\"";
     std::cerr << str << "\"," << (int32_t)idx << "," << (int32_t)len << ") functor.\n";
   } return result;
}
public:
// -- initialize symbol table --
SymbolTable symTable;// -- initialize record table --
RecordTable recordTable;
// -- Table: BasicBlockHead
Own<t_btree_ii__0_1__11__10> rel_1_BasicBlockHead = mk<t_btree_ii__0_1__11__10>();
souffle::RelationWrapper<t_btree_ii__0_1__11__10> wrapper_rel_1_BasicBlockHead;
// -- Table: AssignBinop
Own<t_btree_iiii__0_1_2_3__1000__1111> rel_2_AssignBinop = mk<t_btree_iiii__0_1_2_3__1000__1111>();
souffle::RelationWrapper<t_btree_iiii__0_1_2_3__1000__1111> wrapper_rel_2_AssignBinop;
// -- Table: OperatorAt
Own<t_btree_ii__0_1__11> rel_3_OperatorAt = mk<t_btree_ii__0_1__11>();
souffle::RelationWrapper<t_btree_ii__0_1__11> wrapper_rel_3_OperatorAt;
// -- Table: If
Own<t_btree_iiii__0_1_2_3__1000__1111> rel_4_If = mk<t_btree_iiii__0_1_2_3__1000__1111>();
souffle::RelationWrapper<t_btree_iiii__0_1_2_3__1000__1111> wrapper_rel_4_If;
// -- Table: MayPredecessorBBModuloThrow
Own<t_btree_ii__1_0__0__11__10__01> rel_5_MayPredecessorBBModuloThrow = mk<t_btree_ii__1_0__0__11__10__01>();
souffle::RelationWrapper<t_btree_ii__1_0__0__11__10__01> wrapper_rel_5_MayPredecessorBBModuloThrow;
// -- Table: AssignOperFrom
Own<t_btree_iii__0_1_2__100__120__111> rel_6_AssignOperFrom = mk<t_btree_iii__0_1_2__100__120__111>();
souffle::RelationWrapper<t_btree_iii__0_1_2__100__120__111> wrapper_rel_6_AssignOperFrom;
// -- Table: AssignOperFromConstant
Own<t_btree_iii__0_1_2__100__120__111> rel_7_AssignOperFromConstant = mk<t_btree_iii__0_1_2__100__120__111>();
souffle::RelationWrapper<t_btree_iii__0_1_2__100__120__111> wrapper_rel_7_AssignOperFromConstant;
// -- Table: BinaryExpression
Own<t_btree_iii__0_1_2__111> rel_8_BinaryExpression = mk<t_btree_iii__0_1_2__111>();
souffle::RelationWrapper<t_btree_iii__0_1_2__111> wrapper_rel_8_BinaryExpression;
// -- Table: BasicBlockBegin
Own<t_btree_i__0__1> rel_9_BasicBlockBegin = mk<t_btree_i__0__1>();
souffle::RelationWrapper<t_btree_i__0__1> wrapper_rel_9_BasicBlockBegin;
// -- Table: NrOfPredBB
Own<t_btree_ii__0_1__11__12> rel_10_NrOfPredBB = mk<t_btree_ii__0_1__11__12>();
souffle::RelationWrapper<t_btree_ii__0_1__11__12> wrapper_rel_10_NrOfPredBB;
// -- Table: BinaryExpressionBB
Own<t_btree_ii__1_0__11__01> rel_11_BinaryExpressionBB = mk<t_btree_ii__1_0__11__01>();
souffle::RelationWrapper<t_btree_ii__1_0__11__01> wrapper_rel_11_BinaryExpressionBB;
// -- Table: @delta_BinaryExpressionBB
Own<t_btree_ii__1_0__11__01> rel_12_delta_BinaryExpressionBB = mk<t_btree_ii__1_0__11__01>();
// -- Table: @new_BinaryExpressionBB
Own<t_btree_ii__1_0__11__01> rel_13_new_BinaryExpressionBB = mk<t_btree_ii__1_0__11__01>();
// -- Table: __agg_subclause
Own<t_btree_iii__1_2_0__011__111> rel_14_agg_subclause = mk<t_btree_iii__1_2_0__011__111>();
souffle::RelationWrapper<t_btree_iii__1_2_0__011__111> wrapper_rel_14_agg_subclause;
// -- Table: NoJoinExpressions
Own<t_btree_ii__0_1__11> rel_15_NoJoinExpressions = mk<t_btree_ii__0_1__11>();
souffle::RelationWrapper<t_btree_ii__0_1__11> wrapper_rel_15_NoJoinExpressions;
// -- Table: CommonSubExpression
Own<t_btree_ii__0_1__11> rel_16_CommonSubExpression = mk<t_btree_ii__0_1__11>();
souffle::RelationWrapper<t_btree_ii__0_1__11> wrapper_rel_16_CommonSubExpression;
// -- Table: UnaryExpression
Own<t_btree_iiii__0_1_2_3__1111> rel_17_UnaryExpression = mk<t_btree_iiii__0_1_2_3__1111>();
souffle::RelationWrapper<t_btree_iiii__0_1_2_3__1111> wrapper_rel_17_UnaryExpression;
public:
Sf_AvailableExpressions()
: wrapper_rel_1_BasicBlockHead(0, *rel_1_BasicBlockHead, *this, "BasicBlockHead", std::array<const char *,2>{{"s:Instruction","s:Instruction"}}, std::array<const char *,2>{{"?inst","?ins"}}, 0)
, wrapper_rel_2_AssignBinop(1, *rel_2_AssignBinop, *this, "AssignBinop", std::array<const char *,4>{{"s:Instruction","i:number","s:Var","s:Method"}}, std::array<const char *,4>{{"?instruction","?index","?to","?inmethod"}}, 0)
, wrapper_rel_3_OperatorAt(2, *rel_3_OperatorAt, *this, "OperatorAt", std::array<const char *,2>{{"s:Instruction","s:Operator"}}, std::array<const char *,2>{{"?assign","?op"}}, 0)
, wrapper_rel_4_If(3, *rel_4_If, *this, "If", std::array<const char *,4>{{"s:Instruction","i:number","i:number","s:Method"}}, std::array<const char *,4>{{"?ifNode","?lineNr","?jump","?method"}}, 0)
, wrapper_rel_5_MayPredecessorBBModuloThrow(4, *rel_5_MayPredecessorBBModuloThrow, *this, "MayPredecessorBBModuloThrow", std::array<const char *,2>{{"s:Instruction","s:Instruction"}}, std::array<const char *,2>{{"?inst","?inst1"}}, 0)
, wrapper_rel_6_AssignOperFrom(5, *rel_6_AssignOperFrom, *this, "AssignOperFrom", std::array<const char *,3>{{"s:Instruction","i:number","s:Var"}}, std::array<const char *,3>{{"?instruction","?pos","?from"}}, 0)
, wrapper_rel_7_AssignOperFromConstant(6, *rel_7_AssignOperFromConstant, *this, "AssignOperFromConstant", std::array<const char *,3>{{"s:Instruction","i:number","i:number"}}, std::array<const char *,3>{{"?instruction","?pos","?from"}}, 0)
, wrapper_rel_8_BinaryExpression(7, *rel_8_BinaryExpression, *this, "BinaryExpression", std::array<const char *,3>{{"s:Instruction","r:BinExp","s:Var"}}, std::array<const char *,3>{{"?assign","?b","?to"}}, 0)
, wrapper_rel_9_BasicBlockBegin(8, *rel_9_BasicBlockBegin, *this, "BasicBlockBegin", std::array<const char *,1>{{"s:Instruction"}}, std::array<const char *,1>{{"?ass"}}, 0)
, wrapper_rel_10_NrOfPredBB(9, *rel_10_NrOfPredBB, *this, "NrOfPredBB", std::array<const char *,2>{{"s:Instruction","i:number"}}, std::array<const char *,2>{{"?BB2","?n"}}, 0)
, wrapper_rel_11_BinaryExpressionBB(10, *rel_11_BinaryExpressionBB, *this, "BinaryExpressionBB", std::array<const char *,2>{{"s:Instruction","r:BinExp"}}, std::array<const char *,2>{{"?assign","?exp"}}, 0)
, wrapper_rel_14_agg_subclause(11, *rel_14_agg_subclause, *this, "__agg_subclause", std::array<const char *,3>{{"s:Instruction","s:Instruction","r:BinExp"}}, std::array<const char *,3>{{"?BB2","?BB3","?exp"}}, 0)
, wrapper_rel_15_NoJoinExpressions(12, *rel_15_NoJoinExpressions, *this, "NoJoinExpressions", std::array<const char *,2>{{"s:Instruction","r:BinExp"}}, std::array<const char *,2>{{"?BB1","?exp"}}, 0)
, wrapper_rel_16_CommonSubExpression(13, *rel_16_CommonSubExpression, *this, "CommonSubExpression", std::array<const char *,2>{{"s:Var","s:Var"}}, std::array<const char *,2>{{"?to1","?to2"}}, 0)
, wrapper_rel_17_UnaryExpression(14, *rel_17_UnaryExpression, *this, "UnaryExpression", std::array<const char *,4>{{"s:Instruction","s:Var","s:Operator","s:Var"}}, std::array<const char *,4>{{"?assign","?left","?op","?to"}}, 0)
{
addRelation("BasicBlockHead", wrapper_rel_1_BasicBlockHead, true, false);
addRelation("AssignBinop", wrapper_rel_2_AssignBinop, true, false);
addRelation("OperatorAt", wrapper_rel_3_OperatorAt, true, false);
addRelation("If", wrapper_rel_4_If, true, false);
addRelation("MayPredecessorBBModuloThrow", wrapper_rel_5_MayPredecessorBBModuloThrow, true, false);
addRelation("AssignOperFrom", wrapper_rel_6_AssignOperFrom, true, false);
addRelation("AssignOperFromConstant", wrapper_rel_7_AssignOperFromConstant, true, false);
addRelation("BinaryExpression", wrapper_rel_8_BinaryExpression, false, true);
addRelation("BasicBlockBegin", wrapper_rel_9_BasicBlockBegin, true, false);
addRelation("NrOfPredBB", wrapper_rel_10_NrOfPredBB, false, true);
addRelation("BinaryExpressionBB", wrapper_rel_11_BinaryExpressionBB, false, true);
addRelation("__agg_subclause", wrapper_rel_14_agg_subclause, false, false);
addRelation("NoJoinExpressions", wrapper_rel_15_NoJoinExpressions, false, true);
addRelation("CommonSubExpression", wrapper_rel_16_CommonSubExpression, false, true);
addRelation("UnaryExpression", wrapper_rel_17_UnaryExpression, false, true);
}
~Sf_AvailableExpressions() {
}

private:
std::string             inputDirectory;
std::string             outputDirectory;
SignalHandler*          signalHandler {SignalHandler::instance()};
std::atomic<RamDomain>  ctr {};
std::atomic<std::size_t>     iter {};
bool                    performIO = false;

void runFunction(std::string  inputDirectoryArg   = "",
                 std::string  outputDirectoryArg  = "",
                 bool         performIOArg        = false) {
    this->inputDirectory  = std::move(inputDirectoryArg);
    this->outputDirectory = std::move(outputDirectoryArg);
    this->performIO       = performIOArg;

    // set default threads (in embedded mode)
    // if this is not set, and omp is used, the default omp setting of number of cores is used.
#if defined(_OPENMP)
    if (0 < getNumThreads()) { omp_set_num_threads(getNumThreads()); }
#endif

    signalHandler->set();
// -- query evaluation --
{
 std::vector<RamDomain> args, ret;
subroutine_0(args, ret);
}
{
 std::vector<RamDomain> args, ret;
subroutine_1(args, ret);
}
{
 std::vector<RamDomain> args, ret;
subroutine_7(args, ret);
}
{
 std::vector<RamDomain> args, ret;
subroutine_8(args, ret);
}
{
 std::vector<RamDomain> args, ret;
subroutine_9(args, ret);
}
{
 std::vector<RamDomain> args, ret;
subroutine_10(args, ret);
}
{
 std::vector<RamDomain> args, ret;
subroutine_11(args, ret);
}
{
 std::vector<RamDomain> args, ret;
subroutine_12(args, ret);
}
{
 std::vector<RamDomain> args, ret;
subroutine_13(args, ret);
}
{
 std::vector<RamDomain> args, ret;
subroutine_14(args, ret);
}
{
 std::vector<RamDomain> args, ret;
subroutine_2(args, ret);
}
{
 std::vector<RamDomain> args, ret;
subroutine_3(args, ret);
}
{
 std::vector<RamDomain> args, ret;
subroutine_4(args, ret);
}
{
 std::vector<RamDomain> args, ret;
subroutine_5(args, ret);
}
{
 std::vector<RamDomain> args, ret;
subroutine_6(args, ret);
}

// -- relation hint statistics --
signalHandler->reset();
}
public:
void run() override { runFunction("", "", false); }
public:
void runAll(std::string inputDirectoryArg = "", std::string outputDirectoryArg = "") override { runFunction(inputDirectoryArg, outputDirectoryArg, true);
}
public:
void printAll(std::string outputDirectoryArg = "") override {
try {std::map<std::string, std::string> directiveMap({{"IO","file"},{"attributeNames","?assign\t?b\t?to"},{"auxArity","0"},{"name","BinaryExpression"},{"operation","output"},{"output-dir","Results/AvailableExpressions/"},{"params","{\"records\": {\"BinExp\": {\"arity\": 3, \"params\": [\"?left\", \"?op\", \"?right\"]}}, \"relation\": {\"arity\": 3, \"params\": [\"?assign\", \"?b\", \"?to\"]}}"},{"types","{\"ADTs\": {}, \"records\": {\"r:BinExp\": {\"arity\": 3, \"types\": [\"s:Var\", \"s:Operator\", \"s:Var\"]}}, \"relation\": {\"arity\": 3, \"types\": [\"s:Instruction\", \"r:BinExp\", \"s:Var\"]}}"}});
if (!outputDirectoryArg.empty()) {directiveMap["output-dir"] = outputDirectoryArg;}
IOSystem::getInstance().getWriter(directiveMap, symTable, recordTable)->writeAll(*rel_8_BinaryExpression);
} catch (std::exception& e) {std::cerr << e.what();exit(1);}
try {std::map<std::string, std::string> directiveMap({{"IO","file"},{"attributeNames","?BB2\t?n"},{"auxArity","0"},{"name","NrOfPredBB"},{"operation","output"},{"output-dir","Results/AvailableExpressions/"},{"params","{\"records\": {\"BinExp\": {\"arity\": 3, \"params\": [\"?left\", \"?op\", \"?right\"]}}, \"relation\": {\"arity\": 2, \"params\": [\"?BB2\", \"?n\"]}}"},{"types","{\"ADTs\": {}, \"records\": {\"r:BinExp\": {\"arity\": 3, \"types\": [\"s:Var\", \"s:Operator\", \"s:Var\"]}}, \"relation\": {\"arity\": 2, \"types\": [\"s:Instruction\", \"i:number\"]}}"}});
if (!outputDirectoryArg.empty()) {directiveMap["output-dir"] = outputDirectoryArg;}
IOSystem::getInstance().getWriter(directiveMap, symTable, recordTable)->writeAll(*rel_10_NrOfPredBB);
} catch (std::exception& e) {std::cerr << e.what();exit(1);}
try {std::map<std::string, std::string> directiveMap({{"IO","file"},{"attributeNames","?assign\t?exp"},{"auxArity","0"},{"name","BinaryExpressionBB"},{"operation","output"},{"output-dir","Results/AvailableExpressions/"},{"params","{\"records\": {\"BinExp\": {\"arity\": 3, \"params\": [\"?left\", \"?op\", \"?right\"]}}, \"relation\": {\"arity\": 2, \"params\": [\"?assign\", \"?exp\"]}}"},{"types","{\"ADTs\": {}, \"records\": {\"r:BinExp\": {\"arity\": 3, \"types\": [\"s:Var\", \"s:Operator\", \"s:Var\"]}}, \"relation\": {\"arity\": 2, \"types\": [\"s:Instruction\", \"r:BinExp\"]}}"}});
if (!outputDirectoryArg.empty()) {directiveMap["output-dir"] = outputDirectoryArg;}
IOSystem::getInstance().getWriter(directiveMap, symTable, recordTable)->writeAll(*rel_11_BinaryExpressionBB);
} catch (std::exception& e) {std::cerr << e.what();exit(1);}
try {std::map<std::string, std::string> directiveMap({{"IO","file"},{"attributeNames","?BB1\t?exp"},{"auxArity","0"},{"name","NoJoinExpressions"},{"operation","output"},{"output-dir","Results/AvailableExpressions/"},{"params","{\"records\": {\"BinExp\": {\"arity\": 3, \"params\": [\"?left\", \"?op\", \"?right\"]}}, \"relation\": {\"arity\": 2, \"params\": [\"?BB1\", \"?exp\"]}}"},{"types","{\"ADTs\": {}, \"records\": {\"r:BinExp\": {\"arity\": 3, \"types\": [\"s:Var\", \"s:Operator\", \"s:Var\"]}}, \"relation\": {\"arity\": 2, \"types\": [\"s:Instruction\", \"r:BinExp\"]}}"}});
if (!outputDirectoryArg.empty()) {directiveMap["output-dir"] = outputDirectoryArg;}
IOSystem::getInstance().getWriter(directiveMap, symTable, recordTable)->writeAll(*rel_15_NoJoinExpressions);
} catch (std::exception& e) {std::cerr << e.what();exit(1);}
try {std::map<std::string, std::string> directiveMap({{"IO","file"},{"attributeNames","?to1\t?to2"},{"auxArity","0"},{"name","CommonSubExpression"},{"operation","output"},{"output-dir","Results/AvailableExpressions/"},{"params","{\"records\": {\"BinExp\": {\"arity\": 3, \"params\": [\"?left\", \"?op\", \"?right\"]}}, \"relation\": {\"arity\": 2, \"params\": [\"?to1\", \"?to2\"]}}"},{"types","{\"ADTs\": {}, \"records\": {\"r:BinExp\": {\"arity\": 3, \"types\": [\"s:Var\", \"s:Operator\", \"s:Var\"]}}, \"relation\": {\"arity\": 2, \"types\": [\"s:Var\", \"s:Var\"]}}"}});
if (!outputDirectoryArg.empty()) {directiveMap["output-dir"] = outputDirectoryArg;}
IOSystem::getInstance().getWriter(directiveMap, symTable, recordTable)->writeAll(*rel_16_CommonSubExpression);
} catch (std::exception& e) {std::cerr << e.what();exit(1);}
try {std::map<std::string, std::string> directiveMap({{"IO","file"},{"attributeNames","?assign\t?left\t?op\t?to"},{"auxArity","0"},{"name","UnaryExpression"},{"operation","output"},{"output-dir","Results/AvailableExpressions/"},{"params","{\"records\": {\"BinExp\": {\"arity\": 3, \"params\": [\"?left\", \"?op\", \"?right\"]}}, \"relation\": {\"arity\": 4, \"params\": [\"?assign\", \"?left\", \"?op\", \"?to\"]}}"},{"types","{\"ADTs\": {}, \"records\": {\"r:BinExp\": {\"arity\": 3, \"types\": [\"s:Var\", \"s:Operator\", \"s:Var\"]}}, \"relation\": {\"arity\": 4, \"types\": [\"s:Instruction\", \"s:Var\", \"s:Operator\", \"s:Var\"]}}"}});
if (!outputDirectoryArg.empty()) {directiveMap["output-dir"] = outputDirectoryArg;}
IOSystem::getInstance().getWriter(directiveMap, symTable, recordTable)->writeAll(*rel_17_UnaryExpression);
} catch (std::exception& e) {std::cerr << e.what();exit(1);}
}
public:
void loadAll(std::string inputDirectoryArg = "") override {
try {std::map<std::string, std::string> directiveMap({{"IO","file"},{"attributeNames","?ass"},{"auxArity","0"},{"delimiter","\t"},{"fact-dir","../out/16AvExpr/database"},{"filename","BasicBlockBegin.csv"},{"name","BasicBlockBegin"},{"operation","input"},{"params","{\"records\": {\"BinExp\": {\"arity\": 3, \"params\": [\"?left\", \"?op\", \"?right\"]}}, \"relation\": {\"arity\": 1, \"params\": [\"?ass\"]}}"},{"types","{\"ADTs\": {}, \"records\": {\"r:BinExp\": {\"arity\": 3, \"types\": [\"s:Var\", \"s:Operator\", \"s:Var\"]}}, \"relation\": {\"arity\": 1, \"types\": [\"s:Instruction\"]}}"}});
if (!inputDirectoryArg.empty()) {directiveMap["fact-dir"] = inputDirectoryArg;}
IOSystem::getInstance().getReader(directiveMap, symTable, recordTable)->readAll(*rel_9_BasicBlockBegin);
} catch (std::exception& e) {std::cerr << "Error loading data: " << e.what() << '\n';}
try {std::map<std::string, std::string> directiveMap({{"IO","file"},{"attributeNames","?assign\t?op"},{"auxArity","0"},{"delimter","\t"},{"fact-dir","../out/16AvExpr/database"},{"filename","OperatorAt.facts"},{"name","OperatorAt"},{"operation","input"},{"params","{\"records\": {\"BinExp\": {\"arity\": 3, \"params\": [\"?left\", \"?op\", \"?right\"]}}, \"relation\": {\"arity\": 2, \"params\": [\"?assign\", \"?op\"]}}"},{"types","{\"ADTs\": {}, \"records\": {\"r:BinExp\": {\"arity\": 3, \"types\": [\"s:Var\", \"s:Operator\", \"s:Var\"]}}, \"relation\": {\"arity\": 2, \"types\": [\"s:Instruction\", \"s:Operator\"]}}"}});
if (!inputDirectoryArg.empty()) {directiveMap["fact-dir"] = inputDirectoryArg;}
IOSystem::getInstance().getReader(directiveMap, symTable, recordTable)->readAll(*rel_3_OperatorAt);
} catch (std::exception& e) {std::cerr << "Error loading data: " << e.what() << '\n';}
try {std::map<std::string, std::string> directiveMap({{"IO","file"},{"attributeNames","?ifNode\t?lineNr\t?jump\t?method"},{"auxArity","0"},{"delimiter","\t"},{"fact-dir","../out/16AvExpr/database"},{"filename","If.facts"},{"name","If"},{"operation","input"},{"params","{\"records\": {\"BinExp\": {\"arity\": 3, \"params\": [\"?left\", \"?op\", \"?right\"]}}, \"relation\": {\"arity\": 4, \"params\": [\"?ifNode\", \"?lineNr\", \"?jump\", \"?method\"]}}"},{"types","{\"ADTs\": {}, \"records\": {\"r:BinExp\": {\"arity\": 3, \"types\": [\"s:Var\", \"s:Operator\", \"s:Var\"]}}, \"relation\": {\"arity\": 4, \"types\": [\"s:Instruction\", \"i:number\", \"i:number\", \"s:Method\"]}}"}});
if (!inputDirectoryArg.empty()) {directiveMap["fact-dir"] = inputDirectoryArg;}
IOSystem::getInstance().getReader(directiveMap, symTable, recordTable)->readAll(*rel_4_If);
} catch (std::exception& e) {std::cerr << "Error loading data: " << e.what() << '\n';}
try {std::map<std::string, std::string> directiveMap({{"IO","file"},{"attributeNames","?instruction\t?pos\t?from"},{"auxArity","0"},{"delimiter","\t"},{"fact-dir","../out/16AvExpr/database"},{"filename","AssignOperFromConstant.facts"},{"name","AssignOperFromConstant"},{"operation","input"},{"params","{\"records\": {\"BinExp\": {\"arity\": 3, \"params\": [\"?left\", \"?op\", \"?right\"]}}, \"relation\": {\"arity\": 3, \"params\": [\"?instruction\", \"?pos\", \"?from\"]}}"},{"types","{\"ADTs\": {}, \"records\": {\"r:BinExp\": {\"arity\": 3, \"types\": [\"s:Var\", \"s:Operator\", \"s:Var\"]}}, \"relation\": {\"arity\": 3, \"types\": [\"s:Instruction\", \"i:number\", \"i:number\"]}}"}});
if (!inputDirectoryArg.empty()) {directiveMap["fact-dir"] = inputDirectoryArg;}
IOSystem::getInstance().getReader(directiveMap, symTable, recordTable)->readAll(*rel_7_AssignOperFromConstant);
} catch (std::exception& e) {std::cerr << "Error loading data: " << e.what() << '\n';}
try {std::map<std::string, std::string> directiveMap({{"IO","file"},{"attributeNames","?inst\t?ins"},{"auxArity","0"},{"delimiter","\t"},{"fact-dir","../out/16AvExpr/database"},{"filename","BasicBlockHead.csv"},{"name","BasicBlockHead"},{"operation","input"},{"params","{\"records\": {\"BinExp\": {\"arity\": 3, \"params\": [\"?left\", \"?op\", \"?right\"]}}, \"relation\": {\"arity\": 2, \"params\": [\"?inst\", \"?ins\"]}}"},{"types","{\"ADTs\": {}, \"records\": {\"r:BinExp\": {\"arity\": 3, \"types\": [\"s:Var\", \"s:Operator\", \"s:Var\"]}}, \"relation\": {\"arity\": 2, \"types\": [\"s:Instruction\", \"s:Instruction\"]}}"}});
if (!inputDirectoryArg.empty()) {directiveMap["fact-dir"] = inputDirectoryArg;}
IOSystem::getInstance().getReader(directiveMap, symTable, recordTable)->readAll(*rel_1_BasicBlockHead);
} catch (std::exception& e) {std::cerr << "Error loading data: " << e.what() << '\n';}
try {std::map<std::string, std::string> directiveMap({{"IO","file"},{"attributeNames","?instruction\t?pos\t?from"},{"auxArity","0"},{"delimiter","\t"},{"fact-dir","../out/16AvExpr/database"},{"filename","AssignOperFrom.facts"},{"name","AssignOperFrom"},{"operation","input"},{"params","{\"records\": {\"BinExp\": {\"arity\": 3, \"params\": [\"?left\", \"?op\", \"?right\"]}}, \"relation\": {\"arity\": 3, \"params\": [\"?instruction\", \"?pos\", \"?from\"]}}"},{"types","{\"ADTs\": {}, \"records\": {\"r:BinExp\": {\"arity\": 3, \"types\": [\"s:Var\", \"s:Operator\", \"s:Var\"]}}, \"relation\": {\"arity\": 3, \"types\": [\"s:Instruction\", \"i:number\", \"s:Var\"]}}"}});
if (!inputDirectoryArg.empty()) {directiveMap["fact-dir"] = inputDirectoryArg;}
IOSystem::getInstance().getReader(directiveMap, symTable, recordTable)->readAll(*rel_6_AssignOperFrom);
} catch (std::exception& e) {std::cerr << "Error loading data: " << e.what() << '\n';}
try {std::map<std::string, std::string> directiveMap({{"IO","file"},{"attributeNames","?inst\t?inst1"},{"auxArity","0"},{"delimiter","\t"},{"fact-dir","../out/16AvExpr/database"},{"filename","MayPredecessorBBModuloThrow.csv"},{"name","MayPredecessorBBModuloThrow"},{"operation","input"},{"params","{\"records\": {\"BinExp\": {\"arity\": 3, \"params\": [\"?left\", \"?op\", \"?right\"]}}, \"relation\": {\"arity\": 2, \"params\": [\"?inst\", \"?inst1\"]}}"},{"types","{\"ADTs\": {}, \"records\": {\"r:BinExp\": {\"arity\": 3, \"types\": [\"s:Var\", \"s:Operator\", \"s:Var\"]}}, \"relation\": {\"arity\": 2, \"types\": [\"s:Instruction\", \"s:Instruction\"]}}"}});
if (!inputDirectoryArg.empty()) {directiveMap["fact-dir"] = inputDirectoryArg;}
IOSystem::getInstance().getReader(directiveMap, symTable, recordTable)->readAll(*rel_5_MayPredecessorBBModuloThrow);
} catch (std::exception& e) {std::cerr << "Error loading data: " << e.what() << '\n';}
try {std::map<std::string, std::string> directiveMap({{"IO","file"},{"attributeNames","?instruction\t?index\t?to\t?inmethod"},{"auxArity","0"},{"delimiter","\t"},{"fact-dir","../out/16AvExpr/database"},{"filename","AssignBinop.facts"},{"name","AssignBinop"},{"operation","input"},{"params","{\"records\": {\"BinExp\": {\"arity\": 3, \"params\": [\"?left\", \"?op\", \"?right\"]}}, \"relation\": {\"arity\": 4, \"params\": [\"?instruction\", \"?index\", \"?to\", \"?inmethod\"]}}"},{"types","{\"ADTs\": {}, \"records\": {\"r:BinExp\": {\"arity\": 3, \"types\": [\"s:Var\", \"s:Operator\", \"s:Var\"]}}, \"relation\": {\"arity\": 4, \"types\": [\"s:Instruction\", \"i:number\", \"s:Var\", \"s:Method\"]}}"}});
if (!inputDirectoryArg.empty()) {directiveMap["fact-dir"] = inputDirectoryArg;}
IOSystem::getInstance().getReader(directiveMap, symTable, recordTable)->readAll(*rel_2_AssignBinop);
} catch (std::exception& e) {std::cerr << "Error loading data: " << e.what() << '\n';}
}
public:
void dumpInputs() override {
try {std::map<std::string, std::string> rwOperation;
rwOperation["IO"] = "stdout";
rwOperation["name"] = "BasicBlockBegin";
rwOperation["types"] = "{\"relation\": {\"arity\": 1, \"auxArity\": 0, \"types\": [\"s:Instruction\"]}}";
IOSystem::getInstance().getWriter(rwOperation, symTable, recordTable)->writeAll(*rel_9_BasicBlockBegin);
} catch (std::exception& e) {std::cerr << e.what();exit(1);}
try {std::map<std::string, std::string> rwOperation;
rwOperation["IO"] = "stdout";
rwOperation["name"] = "OperatorAt";
rwOperation["types"] = "{\"relation\": {\"arity\": 2, \"auxArity\": 0, \"types\": [\"s:Instruction\", \"s:Operator\"]}}";
IOSystem::getInstance().getWriter(rwOperation, symTable, recordTable)->writeAll(*rel_3_OperatorAt);
} catch (std::exception& e) {std::cerr << e.what();exit(1);}
try {std::map<std::string, std::string> rwOperation;
rwOperation["IO"] = "stdout";
rwOperation["name"] = "If";
rwOperation["types"] = "{\"relation\": {\"arity\": 4, \"auxArity\": 0, \"types\": [\"s:Instruction\", \"i:number\", \"i:number\", \"s:Method\"]}}";
IOSystem::getInstance().getWriter(rwOperation, symTable, recordTable)->writeAll(*rel_4_If);
} catch (std::exception& e) {std::cerr << e.what();exit(1);}
try {std::map<std::string, std::string> rwOperation;
rwOperation["IO"] = "stdout";
rwOperation["name"] = "AssignOperFromConstant";
rwOperation["types"] = "{\"relation\": {\"arity\": 3, \"auxArity\": 0, \"types\": [\"s:Instruction\", \"i:number\", \"i:number\"]}}";
IOSystem::getInstance().getWriter(rwOperation, symTable, recordTable)->writeAll(*rel_7_AssignOperFromConstant);
} catch (std::exception& e) {std::cerr << e.what();exit(1);}
try {std::map<std::string, std::string> rwOperation;
rwOperation["IO"] = "stdout";
rwOperation["name"] = "BasicBlockHead";
rwOperation["types"] = "{\"relation\": {\"arity\": 2, \"auxArity\": 0, \"types\": [\"s:Instruction\", \"s:Instruction\"]}}";
IOSystem::getInstance().getWriter(rwOperation, symTable, recordTable)->writeAll(*rel_1_BasicBlockHead);
} catch (std::exception& e) {std::cerr << e.what();exit(1);}
try {std::map<std::string, std::string> rwOperation;
rwOperation["IO"] = "stdout";
rwOperation["name"] = "AssignOperFrom";
rwOperation["types"] = "{\"relation\": {\"arity\": 3, \"auxArity\": 0, \"types\": [\"s:Instruction\", \"i:number\", \"s:Var\"]}}";
IOSystem::getInstance().getWriter(rwOperation, symTable, recordTable)->writeAll(*rel_6_AssignOperFrom);
} catch (std::exception& e) {std::cerr << e.what();exit(1);}
try {std::map<std::string, std::string> rwOperation;
rwOperation["IO"] = "stdout";
rwOperation["name"] = "MayPredecessorBBModuloThrow";
rwOperation["types"] = "{\"relation\": {\"arity\": 2, \"auxArity\": 0, \"types\": [\"s:Instruction\", \"s:Instruction\"]}}";
IOSystem::getInstance().getWriter(rwOperation, symTable, recordTable)->writeAll(*rel_5_MayPredecessorBBModuloThrow);
} catch (std::exception& e) {std::cerr << e.what();exit(1);}
try {std::map<std::string, std::string> rwOperation;
rwOperation["IO"] = "stdout";
rwOperation["name"] = "AssignBinop";
rwOperation["types"] = "{\"relation\": {\"arity\": 4, \"auxArity\": 0, \"types\": [\"s:Instruction\", \"i:number\", \"s:Var\", \"s:Method\"]}}";
IOSystem::getInstance().getWriter(rwOperation, symTable, recordTable)->writeAll(*rel_2_AssignBinop);
} catch (std::exception& e) {std::cerr << e.what();exit(1);}
}
public:
void dumpOutputs() override {
try {std::map<std::string, std::string> rwOperation;
rwOperation["IO"] = "stdout";
rwOperation["name"] = "BinaryExpression";
rwOperation["types"] = "{\"relation\": {\"arity\": 3, \"auxArity\": 0, \"types\": [\"s:Instruction\", \"r:BinExp\", \"s:Var\"]}}";
IOSystem::getInstance().getWriter(rwOperation, symTable, recordTable)->writeAll(*rel_8_BinaryExpression);
} catch (std::exception& e) {std::cerr << e.what();exit(1);}
try {std::map<std::string, std::string> rwOperation;
rwOperation["IO"] = "stdout";
rwOperation["name"] = "NrOfPredBB";
rwOperation["types"] = "{\"relation\": {\"arity\": 2, \"auxArity\": 0, \"types\": [\"s:Instruction\", \"i:number\"]}}";
IOSystem::getInstance().getWriter(rwOperation, symTable, recordTable)->writeAll(*rel_10_NrOfPredBB);
} catch (std::exception& e) {std::cerr << e.what();exit(1);}
try {std::map<std::string, std::string> rwOperation;
rwOperation["IO"] = "stdout";
rwOperation["name"] = "BinaryExpressionBB";
rwOperation["types"] = "{\"relation\": {\"arity\": 2, \"auxArity\": 0, \"types\": [\"s:Instruction\", \"r:BinExp\"]}}";
IOSystem::getInstance().getWriter(rwOperation, symTable, recordTable)->writeAll(*rel_11_BinaryExpressionBB);
} catch (std::exception& e) {std::cerr << e.what();exit(1);}
try {std::map<std::string, std::string> rwOperation;
rwOperation["IO"] = "stdout";
rwOperation["name"] = "NoJoinExpressions";
rwOperation["types"] = "{\"relation\": {\"arity\": 2, \"auxArity\": 0, \"types\": [\"s:Instruction\", \"r:BinExp\"]}}";
IOSystem::getInstance().getWriter(rwOperation, symTable, recordTable)->writeAll(*rel_15_NoJoinExpressions);
} catch (std::exception& e) {std::cerr << e.what();exit(1);}
try {std::map<std::string, std::string> rwOperation;
rwOperation["IO"] = "stdout";
rwOperation["name"] = "CommonSubExpression";
rwOperation["types"] = "{\"relation\": {\"arity\": 2, \"auxArity\": 0, \"types\": [\"s:Var\", \"s:Var\"]}}";
IOSystem::getInstance().getWriter(rwOperation, symTable, recordTable)->writeAll(*rel_16_CommonSubExpression);
} catch (std::exception& e) {std::cerr << e.what();exit(1);}
try {std::map<std::string, std::string> rwOperation;
rwOperation["IO"] = "stdout";
rwOperation["name"] = "UnaryExpression";
rwOperation["types"] = "{\"relation\": {\"arity\": 4, \"auxArity\": 0, \"types\": [\"s:Instruction\", \"s:Var\", \"s:Operator\", \"s:Var\"]}}";
IOSystem::getInstance().getWriter(rwOperation, symTable, recordTable)->writeAll(*rel_17_UnaryExpression);
} catch (std::exception& e) {std::cerr << e.what();exit(1);}
}
public:
SymbolTable& getSymbolTable() override {
return symTable;
}
RecordTable& getRecordTable() override {
return recordTable;
}
void setNumThreads(std::size_t numThreadsValue) override {
SouffleProgram::setNumThreads(numThreadsValue);
symTable.setNumLanes(getNumThreads());
recordTable.setNumLanes(getNumThreads());
}
void executeSubroutine(std::string name, const std::vector<RamDomain>& args, std::vector<RamDomain>& ret) override {
if (name == "stratum_0") {
subroutine_0(args, ret);
return;}
if (name == "stratum_1") {
subroutine_1(args, ret);
return;}
if (name == "stratum_10") {
subroutine_2(args, ret);
return;}
if (name == "stratum_11") {
subroutine_3(args, ret);
return;}
if (name == "stratum_12") {
subroutine_4(args, ret);
return;}
if (name == "stratum_13") {
subroutine_5(args, ret);
return;}
if (name == "stratum_14") {
subroutine_6(args, ret);
return;}
if (name == "stratum_2") {
subroutine_7(args, ret);
return;}
if (name == "stratum_3") {
subroutine_8(args, ret);
return;}
if (name == "stratum_4") {
subroutine_9(args, ret);
return;}
if (name == "stratum_5") {
subroutine_10(args, ret);
return;}
if (name == "stratum_6") {
subroutine_11(args, ret);
return;}
if (name == "stratum_7") {
subroutine_12(args, ret);
return;}
if (name == "stratum_8") {
subroutine_13(args, ret);
return;}
if (name == "stratum_9") {
subroutine_14(args, ret);
return;}
fatal("unknown subroutine");
}
#ifdef _MSC_VER
#pragma warning(disable: 4100)
#endif // _MSC_VER
void subroutine_0(const std::vector<RamDomain>& args, std::vector<RamDomain>& ret) {
if (performIO) {
try {std::map<std::string, std::string> directiveMap({{"IO","file"},{"attributeNames","?inst\t?ins"},{"auxArity","0"},{"delimiter","\t"},{"fact-dir","../out/16AvExpr/database"},{"filename","BasicBlockHead.csv"},{"name","BasicBlockHead"},{"operation","input"},{"params","{\"records\": {\"BinExp\": {\"arity\": 3, \"params\": [\"?left\", \"?op\", \"?right\"]}}, \"relation\": {\"arity\": 2, \"params\": [\"?inst\", \"?ins\"]}}"},{"types","{\"ADTs\": {}, \"records\": {\"r:BinExp\": {\"arity\": 3, \"types\": [\"s:Var\", \"s:Operator\", \"s:Var\"]}}, \"relation\": {\"arity\": 2, \"types\": [\"s:Instruction\", \"s:Instruction\"]}}"}});
if (!inputDirectory.empty()) {directiveMap["fact-dir"] = inputDirectory;}
IOSystem::getInstance().getReader(directiveMap, symTable, recordTable)->readAll(*rel_1_BasicBlockHead);
} catch (std::exception& e) {std::cerr << "Error loading data: " << e.what() << '\n';}
}
}
#ifdef _MSC_VER
#pragma warning(default: 4100)
#endif // _MSC_VER
#ifdef _MSC_VER
#pragma warning(disable: 4100)
#endif // _MSC_VER
void subroutine_1(const std::vector<RamDomain>& args, std::vector<RamDomain>& ret) {
if (performIO) {
try {std::map<std::string, std::string> directiveMap({{"IO","file"},{"attributeNames","?instruction\t?index\t?to\t?inmethod"},{"auxArity","0"},{"delimiter","\t"},{"fact-dir","../out/16AvExpr/database"},{"filename","AssignBinop.facts"},{"name","AssignBinop"},{"operation","input"},{"params","{\"records\": {\"BinExp\": {\"arity\": 3, \"params\": [\"?left\", \"?op\", \"?right\"]}}, \"relation\": {\"arity\": 4, \"params\": [\"?instruction\", \"?index\", \"?to\", \"?inmethod\"]}}"},{"types","{\"ADTs\": {}, \"records\": {\"r:BinExp\": {\"arity\": 3, \"types\": [\"s:Var\", \"s:Operator\", \"s:Var\"]}}, \"relation\": {\"arity\": 4, \"types\": [\"s:Instruction\", \"i:number\", \"s:Var\", \"s:Method\"]}}"}});
if (!inputDirectory.empty()) {directiveMap["fact-dir"] = inputDirectory;}
IOSystem::getInstance().getReader(directiveMap, symTable, recordTable)->readAll(*rel_2_AssignBinop);
} catch (std::exception& e) {std::cerr << "Error loading data: " << e.what() << '\n';}
}
}
#ifdef _MSC_VER
#pragma warning(default: 4100)
#endif // _MSC_VER
#ifdef _MSC_VER
#pragma warning(disable: 4100)
#endif // _MSC_VER
void subroutine_2(const std::vector<RamDomain>& args, std::vector<RamDomain>& ret) {
signalHandler->setMsg(R"_(BinaryExpressionBB(?head,?exp) :- 
   BinaryExpression(?assign,?exp,_),
   BasicBlockHead(?assign,?head).
in file /home/kotname/Documents/10_Semester/INF_PM_ANW/doop/master/TestKnut/Analysis/AvailableExpressions.dl [91:1-93:36])_");
if(!(rel_8_BinaryExpression->empty()) && !(rel_1_BasicBlockHead->empty())) {
[&](){
CREATE_OP_CONTEXT(rel_1_BasicBlockHead_op_ctxt,rel_1_BasicBlockHead->createContext());
CREATE_OP_CONTEXT(rel_8_BinaryExpression_op_ctxt,rel_8_BinaryExpression->createContext());
CREATE_OP_CONTEXT(rel_11_BinaryExpressionBB_op_ctxt,rel_11_BinaryExpressionBB->createContext());
for(const auto& env0 : *rel_8_BinaryExpression) {
auto range = rel_1_BasicBlockHead->lowerUpperRange_10(Tuple<RamDomain,2>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MIN_RAM_SIGNED)}},Tuple<RamDomain,2>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MAX_RAM_SIGNED)}},READ_OP_CONTEXT(rel_1_BasicBlockHead_op_ctxt));
for(const auto& env1 : range) {
Tuple<RamDomain,2> tuple{{ramBitCast(env1[1]),ramBitCast(env0[1])}};
rel_11_BinaryExpressionBB->insert(tuple,READ_OP_CONTEXT(rel_11_BinaryExpressionBB_op_ctxt));
}
}
}
();}
[&](){
CREATE_OP_CONTEXT(rel_11_BinaryExpressionBB_op_ctxt,rel_11_BinaryExpressionBB->createContext());
CREATE_OP_CONTEXT(rel_12_delta_BinaryExpressionBB_op_ctxt,rel_12_delta_BinaryExpressionBB->createContext());
for(const auto& env0 : *rel_11_BinaryExpressionBB) {
Tuple<RamDomain,2> tuple{{ramBitCast(env0[0]),ramBitCast(env0[1])}};
rel_12_delta_BinaryExpressionBB->insert(tuple,READ_OP_CONTEXT(rel_12_delta_BinaryExpressionBB_op_ctxt));
}
}
();iter = 0;
for(;;) {
signalHandler->setMsg(R"_(BinaryExpressionBB(?BB2,?exp) :- 
   BinaryExpressionBB(?BB1,?exp),
   MayPredecessorBBModuloThrow(?BB1,?BB2),
   NrOfPredBB(?BB2,1).
in file /home/kotname/Documents/10_Semester/INF_PM_ANW/doop/master/TestKnut/Analysis/AvailableExpressions.dl [95:1-98:24])_");
if(!(rel_5_MayPredecessorBBModuloThrow->empty()) && !(rel_10_NrOfPredBB->empty()) && !(rel_12_delta_BinaryExpressionBB->empty())) {
[&](){
CREATE_OP_CONTEXT(rel_5_MayPredecessorBBModuloThrow_op_ctxt,rel_5_MayPredecessorBBModuloThrow->createContext());
CREATE_OP_CONTEXT(rel_10_NrOfPredBB_op_ctxt,rel_10_NrOfPredBB->createContext());
CREATE_OP_CONTEXT(rel_11_BinaryExpressionBB_op_ctxt,rel_11_BinaryExpressionBB->createContext());
CREATE_OP_CONTEXT(rel_12_delta_BinaryExpressionBB_op_ctxt,rel_12_delta_BinaryExpressionBB->createContext());
CREATE_OP_CONTEXT(rel_13_new_BinaryExpressionBB_op_ctxt,rel_13_new_BinaryExpressionBB->createContext());
for(const auto& env0 : *rel_12_delta_BinaryExpressionBB) {
auto range = rel_5_MayPredecessorBBModuloThrow->lowerUpperRange_10(Tuple<RamDomain,2>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MIN_RAM_SIGNED)}},Tuple<RamDomain,2>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MAX_RAM_SIGNED)}},READ_OP_CONTEXT(rel_5_MayPredecessorBBModuloThrow_op_ctxt));
for(const auto& env1 : range) {
if( rel_10_NrOfPredBB->contains(Tuple<RamDomain,2>{{ramBitCast(env1[1]),ramBitCast(RamSigned(1))}},READ_OP_CONTEXT(rel_10_NrOfPredBB_op_ctxt)) && !(rel_11_BinaryExpressionBB->contains(Tuple<RamDomain,2>{{ramBitCast(env1[1]),ramBitCast(env0[1])}},READ_OP_CONTEXT(rel_11_BinaryExpressionBB_op_ctxt)))) {
Tuple<RamDomain,2> tuple{{ramBitCast(env1[1]),ramBitCast(env0[1])}};
rel_13_new_BinaryExpressionBB->insert(tuple,READ_OP_CONTEXT(rel_13_new_BinaryExpressionBB_op_ctxt));
}
}
}
}
();}
signalHandler->setMsg(R"_(BinaryExpressionBB(?BB3,?exp) :- 
   BinaryExpressionBB(?BB1,?exp),
   MayPredecessorBBModuloThrow(?BB1,?BB3),
   NrOfPredBB(?BB3,2),
   BinaryExpressionBB(?BB2,?exp),
   ?BB1 != ?BB2,
   MayPredecessorBBModuloThrow(?BB2,?BB3).
in file /home/kotname/Documents/10_Semester/INF_PM_ANW/doop/master/TestKnut/Analysis/AvailableExpressions.dl [100:1-106:44])_");
if(!(rel_11_BinaryExpressionBB->empty()) && !(rel_10_NrOfPredBB->empty()) && !(rel_5_MayPredecessorBBModuloThrow->empty()) && !(rel_12_delta_BinaryExpressionBB->empty())) {
[&](){
CREATE_OP_CONTEXT(rel_5_MayPredecessorBBModuloThrow_op_ctxt,rel_5_MayPredecessorBBModuloThrow->createContext());
CREATE_OP_CONTEXT(rel_10_NrOfPredBB_op_ctxt,rel_10_NrOfPredBB->createContext());
CREATE_OP_CONTEXT(rel_11_BinaryExpressionBB_op_ctxt,rel_11_BinaryExpressionBB->createContext());
CREATE_OP_CONTEXT(rel_12_delta_BinaryExpressionBB_op_ctxt,rel_12_delta_BinaryExpressionBB->createContext());
CREATE_OP_CONTEXT(rel_13_new_BinaryExpressionBB_op_ctxt,rel_13_new_BinaryExpressionBB->createContext());
for(const auto& env0 : *rel_12_delta_BinaryExpressionBB) {
auto range = rel_5_MayPredecessorBBModuloThrow->lowerUpperRange_10(Tuple<RamDomain,2>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MIN_RAM_SIGNED)}},Tuple<RamDomain,2>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MAX_RAM_SIGNED)}},READ_OP_CONTEXT(rel_5_MayPredecessorBBModuloThrow_op_ctxt));
for(const auto& env1 : range) {
if( rel_10_NrOfPredBB->contains(Tuple<RamDomain,2>{{ramBitCast(env1[1]),ramBitCast(RamSigned(2))}},READ_OP_CONTEXT(rel_10_NrOfPredBB_op_ctxt)) && !(rel_11_BinaryExpressionBB->contains(Tuple<RamDomain,2>{{ramBitCast(env1[1]),ramBitCast(env0[1])}},READ_OP_CONTEXT(rel_11_BinaryExpressionBB_op_ctxt)))) {
auto range = rel_11_BinaryExpressionBB->lowerUpperRange_01(Tuple<RamDomain,2>{{ramBitCast<RamDomain>(MIN_RAM_SIGNED), ramBitCast(env0[1])}},Tuple<RamDomain,2>{{ramBitCast<RamDomain>(MAX_RAM_SIGNED), ramBitCast(env0[1])}},READ_OP_CONTEXT(rel_11_BinaryExpressionBB_op_ctxt));
for(const auto& env2 : range) {
if( (ramBitCast<RamDomain>(env0[0]) != ramBitCast<RamDomain>(env2[0])) && rel_5_MayPredecessorBBModuloThrow->contains(Tuple<RamDomain,2>{{ramBitCast(env2[0]),ramBitCast(env1[1])}},READ_OP_CONTEXT(rel_5_MayPredecessorBBModuloThrow_op_ctxt)) && !(rel_12_delta_BinaryExpressionBB->contains(Tuple<RamDomain,2>{{ramBitCast(env2[0]),ramBitCast(env0[1])}},READ_OP_CONTEXT(rel_12_delta_BinaryExpressionBB_op_ctxt)))) {
Tuple<RamDomain,2> tuple{{ramBitCast(env1[1]),ramBitCast(env0[1])}};
rel_13_new_BinaryExpressionBB->insert(tuple,READ_OP_CONTEXT(rel_13_new_BinaryExpressionBB_op_ctxt));
}
}
}
}
}
}
();}
signalHandler->setMsg(R"_(BinaryExpressionBB(?BB3,?exp) :- 
   BinaryExpressionBB(?BB1,?exp),
   MayPredecessorBBModuloThrow(?BB1,?BB3),
   NrOfPredBB(?BB3,2),
   BinaryExpressionBB(?BB2,?exp),
   ?BB1 != ?BB2,
   MayPredecessorBBModuloThrow(?BB2,?BB3).
in file /home/kotname/Documents/10_Semester/INF_PM_ANW/doop/master/TestKnut/Analysis/AvailableExpressions.dl [100:1-106:44])_");
if(!(rel_12_delta_BinaryExpressionBB->empty()) && !(rel_10_NrOfPredBB->empty()) && !(rel_5_MayPredecessorBBModuloThrow->empty()) && !(rel_11_BinaryExpressionBB->empty())) {
[&](){
CREATE_OP_CONTEXT(rel_5_MayPredecessorBBModuloThrow_op_ctxt,rel_5_MayPredecessorBBModuloThrow->createContext());
CREATE_OP_CONTEXT(rel_10_NrOfPredBB_op_ctxt,rel_10_NrOfPredBB->createContext());
CREATE_OP_CONTEXT(rel_11_BinaryExpressionBB_op_ctxt,rel_11_BinaryExpressionBB->createContext());
CREATE_OP_CONTEXT(rel_12_delta_BinaryExpressionBB_op_ctxt,rel_12_delta_BinaryExpressionBB->createContext());
CREATE_OP_CONTEXT(rel_13_new_BinaryExpressionBB_op_ctxt,rel_13_new_BinaryExpressionBB->createContext());
for(const auto& env0 : *rel_11_BinaryExpressionBB) {
auto range = rel_5_MayPredecessorBBModuloThrow->lowerUpperRange_10(Tuple<RamDomain,2>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MIN_RAM_SIGNED)}},Tuple<RamDomain,2>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MAX_RAM_SIGNED)}},READ_OP_CONTEXT(rel_5_MayPredecessorBBModuloThrow_op_ctxt));
for(const auto& env1 : range) {
if( rel_10_NrOfPredBB->contains(Tuple<RamDomain,2>{{ramBitCast(env1[1]),ramBitCast(RamSigned(2))}},READ_OP_CONTEXT(rel_10_NrOfPredBB_op_ctxt)) && !(rel_11_BinaryExpressionBB->contains(Tuple<RamDomain,2>{{ramBitCast(env1[1]),ramBitCast(env0[1])}},READ_OP_CONTEXT(rel_11_BinaryExpressionBB_op_ctxt)))) {
auto range = rel_12_delta_BinaryExpressionBB->lowerUpperRange_01(Tuple<RamDomain,2>{{ramBitCast<RamDomain>(MIN_RAM_SIGNED), ramBitCast(env0[1])}},Tuple<RamDomain,2>{{ramBitCast<RamDomain>(MAX_RAM_SIGNED), ramBitCast(env0[1])}},READ_OP_CONTEXT(rel_12_delta_BinaryExpressionBB_op_ctxt));
for(const auto& env2 : range) {
if( (ramBitCast<RamDomain>(env0[0]) != ramBitCast<RamDomain>(env2[0])) && rel_5_MayPredecessorBBModuloThrow->contains(Tuple<RamDomain,2>{{ramBitCast(env2[0]),ramBitCast(env1[1])}},READ_OP_CONTEXT(rel_5_MayPredecessorBBModuloThrow_op_ctxt))) {
Tuple<RamDomain,2> tuple{{ramBitCast(env1[1]),ramBitCast(env0[1])}};
rel_13_new_BinaryExpressionBB->insert(tuple,READ_OP_CONTEXT(rel_13_new_BinaryExpressionBB_op_ctxt));
}
}
}
}
}
}
();}
signalHandler->setMsg(R"_(BinaryExpressionBB(?BB4,?exp) :- 
   BinaryExpressionBB(?BB1,?exp),
   MayPredecessorBBModuloThrow(?BB1,?BB4),
   NrOfPredBB(?BB4,3),
   BinaryExpressionBB(?BB2,?exp),
   ?BB1 != ?BB2,
   MayPredecessorBBModuloThrow(?BB2,?BB4),
   BinaryExpressionBB(?BB3,?exp),
   ?BB1 != ?BB3,
   ?BB2 != ?BB3,
   MayPredecessorBBModuloThrow(?BB3,?BB4).
in file /home/kotname/Documents/10_Semester/INF_PM_ANW/doop/master/TestKnut/Analysis/AvailableExpressions.dl [109:1-119:44])_");
if(!(rel_11_BinaryExpressionBB->empty()) && !(rel_10_NrOfPredBB->empty()) && !(rel_5_MayPredecessorBBModuloThrow->empty()) && !(rel_12_delta_BinaryExpressionBB->empty())) {
[&](){
CREATE_OP_CONTEXT(rel_5_MayPredecessorBBModuloThrow_op_ctxt,rel_5_MayPredecessorBBModuloThrow->createContext());
CREATE_OP_CONTEXT(rel_10_NrOfPredBB_op_ctxt,rel_10_NrOfPredBB->createContext());
CREATE_OP_CONTEXT(rel_11_BinaryExpressionBB_op_ctxt,rel_11_BinaryExpressionBB->createContext());
CREATE_OP_CONTEXT(rel_12_delta_BinaryExpressionBB_op_ctxt,rel_12_delta_BinaryExpressionBB->createContext());
CREATE_OP_CONTEXT(rel_13_new_BinaryExpressionBB_op_ctxt,rel_13_new_BinaryExpressionBB->createContext());
for(const auto& env0 : *rel_12_delta_BinaryExpressionBB) {
auto range = rel_5_MayPredecessorBBModuloThrow->lowerUpperRange_10(Tuple<RamDomain,2>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MIN_RAM_SIGNED)}},Tuple<RamDomain,2>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MAX_RAM_SIGNED)}},READ_OP_CONTEXT(rel_5_MayPredecessorBBModuloThrow_op_ctxt));
for(const auto& env1 : range) {
if( rel_10_NrOfPredBB->contains(Tuple<RamDomain,2>{{ramBitCast(env1[1]),ramBitCast(RamSigned(3))}},READ_OP_CONTEXT(rel_10_NrOfPredBB_op_ctxt)) && !(rel_11_BinaryExpressionBB->contains(Tuple<RamDomain,2>{{ramBitCast(env1[1]),ramBitCast(env0[1])}},READ_OP_CONTEXT(rel_11_BinaryExpressionBB_op_ctxt)))) {
auto range = rel_11_BinaryExpressionBB->lowerUpperRange_01(Tuple<RamDomain,2>{{ramBitCast<RamDomain>(MIN_RAM_SIGNED), ramBitCast(env0[1])}},Tuple<RamDomain,2>{{ramBitCast<RamDomain>(MAX_RAM_SIGNED), ramBitCast(env0[1])}},READ_OP_CONTEXT(rel_11_BinaryExpressionBB_op_ctxt));
for(const auto& env2 : range) {
if( (ramBitCast<RamDomain>(env0[0]) != ramBitCast<RamDomain>(env2[0])) && rel_5_MayPredecessorBBModuloThrow->contains(Tuple<RamDomain,2>{{ramBitCast(env2[0]),ramBitCast(env1[1])}},READ_OP_CONTEXT(rel_5_MayPredecessorBBModuloThrow_op_ctxt)) && !(rel_12_delta_BinaryExpressionBB->contains(Tuple<RamDomain,2>{{ramBitCast(env2[0]),ramBitCast(env0[1])}},READ_OP_CONTEXT(rel_12_delta_BinaryExpressionBB_op_ctxt)))) {
auto range = rel_11_BinaryExpressionBB->lowerUpperRange_01(Tuple<RamDomain,2>{{ramBitCast<RamDomain>(MIN_RAM_SIGNED), ramBitCast(env0[1])}},Tuple<RamDomain,2>{{ramBitCast<RamDomain>(MAX_RAM_SIGNED), ramBitCast(env0[1])}},READ_OP_CONTEXT(rel_11_BinaryExpressionBB_op_ctxt));
for(const auto& env3 : range) {
if( (ramBitCast<RamDomain>(env2[0]) != ramBitCast<RamDomain>(env3[0])) && (ramBitCast<RamDomain>(env0[0]) != ramBitCast<RamDomain>(env3[0])) && rel_5_MayPredecessorBBModuloThrow->contains(Tuple<RamDomain,2>{{ramBitCast(env3[0]),ramBitCast(env1[1])}},READ_OP_CONTEXT(rel_5_MayPredecessorBBModuloThrow_op_ctxt)) && !(rel_12_delta_BinaryExpressionBB->contains(Tuple<RamDomain,2>{{ramBitCast(env3[0]),ramBitCast(env0[1])}},READ_OP_CONTEXT(rel_12_delta_BinaryExpressionBB_op_ctxt)))) {
Tuple<RamDomain,2> tuple{{ramBitCast(env1[1]),ramBitCast(env0[1])}};
rel_13_new_BinaryExpressionBB->insert(tuple,READ_OP_CONTEXT(rel_13_new_BinaryExpressionBB_op_ctxt));
}
}
}
}
}
}
}
}
();}
signalHandler->setMsg(R"_(BinaryExpressionBB(?BB4,?exp) :- 
   BinaryExpressionBB(?BB1,?exp),
   MayPredecessorBBModuloThrow(?BB1,?BB4),
   NrOfPredBB(?BB4,3),
   BinaryExpressionBB(?BB2,?exp),
   ?BB1 != ?BB2,
   MayPredecessorBBModuloThrow(?BB2,?BB4),
   BinaryExpressionBB(?BB3,?exp),
   ?BB1 != ?BB3,
   ?BB2 != ?BB3,
   MayPredecessorBBModuloThrow(?BB3,?BB4).
in file /home/kotname/Documents/10_Semester/INF_PM_ANW/doop/master/TestKnut/Analysis/AvailableExpressions.dl [109:1-119:44])_");
if(!(rel_11_BinaryExpressionBB->empty()) && !(rel_12_delta_BinaryExpressionBB->empty()) && !(rel_5_MayPredecessorBBModuloThrow->empty()) && !(rel_10_NrOfPredBB->empty())) {
[&](){
CREATE_OP_CONTEXT(rel_5_MayPredecessorBBModuloThrow_op_ctxt,rel_5_MayPredecessorBBModuloThrow->createContext());
CREATE_OP_CONTEXT(rel_10_NrOfPredBB_op_ctxt,rel_10_NrOfPredBB->createContext());
CREATE_OP_CONTEXT(rel_11_BinaryExpressionBB_op_ctxt,rel_11_BinaryExpressionBB->createContext());
CREATE_OP_CONTEXT(rel_12_delta_BinaryExpressionBB_op_ctxt,rel_12_delta_BinaryExpressionBB->createContext());
CREATE_OP_CONTEXT(rel_13_new_BinaryExpressionBB_op_ctxt,rel_13_new_BinaryExpressionBB->createContext());
for(const auto& env0 : *rel_11_BinaryExpressionBB) {
auto range = rel_5_MayPredecessorBBModuloThrow->lowerUpperRange_10(Tuple<RamDomain,2>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MIN_RAM_SIGNED)}},Tuple<RamDomain,2>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MAX_RAM_SIGNED)}},READ_OP_CONTEXT(rel_5_MayPredecessorBBModuloThrow_op_ctxt));
for(const auto& env1 : range) {
if( rel_10_NrOfPredBB->contains(Tuple<RamDomain,2>{{ramBitCast(env1[1]),ramBitCast(RamSigned(3))}},READ_OP_CONTEXT(rel_10_NrOfPredBB_op_ctxt)) && !(rel_11_BinaryExpressionBB->contains(Tuple<RamDomain,2>{{ramBitCast(env1[1]),ramBitCast(env0[1])}},READ_OP_CONTEXT(rel_11_BinaryExpressionBB_op_ctxt)))) {
auto range = rel_12_delta_BinaryExpressionBB->lowerUpperRange_01(Tuple<RamDomain,2>{{ramBitCast<RamDomain>(MIN_RAM_SIGNED), ramBitCast(env0[1])}},Tuple<RamDomain,2>{{ramBitCast<RamDomain>(MAX_RAM_SIGNED), ramBitCast(env0[1])}},READ_OP_CONTEXT(rel_12_delta_BinaryExpressionBB_op_ctxt));
for(const auto& env2 : range) {
if( (ramBitCast<RamDomain>(env0[0]) != ramBitCast<RamDomain>(env2[0])) && rel_5_MayPredecessorBBModuloThrow->contains(Tuple<RamDomain,2>{{ramBitCast(env2[0]),ramBitCast(env1[1])}},READ_OP_CONTEXT(rel_5_MayPredecessorBBModuloThrow_op_ctxt))) {
auto range = rel_11_BinaryExpressionBB->lowerUpperRange_01(Tuple<RamDomain,2>{{ramBitCast<RamDomain>(MIN_RAM_SIGNED), ramBitCast(env0[1])}},Tuple<RamDomain,2>{{ramBitCast<RamDomain>(MAX_RAM_SIGNED), ramBitCast(env0[1])}},READ_OP_CONTEXT(rel_11_BinaryExpressionBB_op_ctxt));
for(const auto& env3 : range) {
if( (ramBitCast<RamDomain>(env0[0]) != ramBitCast<RamDomain>(env3[0])) && (ramBitCast<RamDomain>(env2[0]) != ramBitCast<RamDomain>(env3[0])) && rel_5_MayPredecessorBBModuloThrow->contains(Tuple<RamDomain,2>{{ramBitCast(env3[0]),ramBitCast(env1[1])}},READ_OP_CONTEXT(rel_5_MayPredecessorBBModuloThrow_op_ctxt)) && !(rel_12_delta_BinaryExpressionBB->contains(Tuple<RamDomain,2>{{ramBitCast(env3[0]),ramBitCast(env0[1])}},READ_OP_CONTEXT(rel_12_delta_BinaryExpressionBB_op_ctxt)))) {
Tuple<RamDomain,2> tuple{{ramBitCast(env1[1]),ramBitCast(env0[1])}};
rel_13_new_BinaryExpressionBB->insert(tuple,READ_OP_CONTEXT(rel_13_new_BinaryExpressionBB_op_ctxt));
}
}
}
}
}
}
}
}
();}
signalHandler->setMsg(R"_(BinaryExpressionBB(?BB4,?exp) :- 
   BinaryExpressionBB(?BB1,?exp),
   MayPredecessorBBModuloThrow(?BB1,?BB4),
   NrOfPredBB(?BB4,3),
   BinaryExpressionBB(?BB2,?exp),
   ?BB1 != ?BB2,
   MayPredecessorBBModuloThrow(?BB2,?BB4),
   BinaryExpressionBB(?BB3,?exp),
   ?BB1 != ?BB3,
   ?BB2 != ?BB3,
   MayPredecessorBBModuloThrow(?BB3,?BB4).
in file /home/kotname/Documents/10_Semester/INF_PM_ANW/doop/master/TestKnut/Analysis/AvailableExpressions.dl [109:1-119:44])_");
if(!(rel_12_delta_BinaryExpressionBB->empty()) && !(rel_11_BinaryExpressionBB->empty()) && !(rel_5_MayPredecessorBBModuloThrow->empty()) && !(rel_10_NrOfPredBB->empty())) {
[&](){
CREATE_OP_CONTEXT(rel_5_MayPredecessorBBModuloThrow_op_ctxt,rel_5_MayPredecessorBBModuloThrow->createContext());
CREATE_OP_CONTEXT(rel_10_NrOfPredBB_op_ctxt,rel_10_NrOfPredBB->createContext());
CREATE_OP_CONTEXT(rel_11_BinaryExpressionBB_op_ctxt,rel_11_BinaryExpressionBB->createContext());
CREATE_OP_CONTEXT(rel_12_delta_BinaryExpressionBB_op_ctxt,rel_12_delta_BinaryExpressionBB->createContext());
CREATE_OP_CONTEXT(rel_13_new_BinaryExpressionBB_op_ctxt,rel_13_new_BinaryExpressionBB->createContext());
for(const auto& env0 : *rel_11_BinaryExpressionBB) {
auto range = rel_5_MayPredecessorBBModuloThrow->lowerUpperRange_10(Tuple<RamDomain,2>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MIN_RAM_SIGNED)}},Tuple<RamDomain,2>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MAX_RAM_SIGNED)}},READ_OP_CONTEXT(rel_5_MayPredecessorBBModuloThrow_op_ctxt));
for(const auto& env1 : range) {
if( rel_10_NrOfPredBB->contains(Tuple<RamDomain,2>{{ramBitCast(env1[1]),ramBitCast(RamSigned(3))}},READ_OP_CONTEXT(rel_10_NrOfPredBB_op_ctxt)) && !(rel_11_BinaryExpressionBB->contains(Tuple<RamDomain,2>{{ramBitCast(env1[1]),ramBitCast(env0[1])}},READ_OP_CONTEXT(rel_11_BinaryExpressionBB_op_ctxt)))) {
auto range = rel_11_BinaryExpressionBB->lowerUpperRange_01(Tuple<RamDomain,2>{{ramBitCast<RamDomain>(MIN_RAM_SIGNED), ramBitCast(env0[1])}},Tuple<RamDomain,2>{{ramBitCast<RamDomain>(MAX_RAM_SIGNED), ramBitCast(env0[1])}},READ_OP_CONTEXT(rel_11_BinaryExpressionBB_op_ctxt));
for(const auto& env2 : range) {
if( (ramBitCast<RamDomain>(env0[0]) != ramBitCast<RamDomain>(env2[0])) && rel_5_MayPredecessorBBModuloThrow->contains(Tuple<RamDomain,2>{{ramBitCast(env2[0]),ramBitCast(env1[1])}},READ_OP_CONTEXT(rel_5_MayPredecessorBBModuloThrow_op_ctxt))) {
auto range = rel_12_delta_BinaryExpressionBB->lowerUpperRange_01(Tuple<RamDomain,2>{{ramBitCast<RamDomain>(MIN_RAM_SIGNED), ramBitCast(env0[1])}},Tuple<RamDomain,2>{{ramBitCast<RamDomain>(MAX_RAM_SIGNED), ramBitCast(env0[1])}},READ_OP_CONTEXT(rel_12_delta_BinaryExpressionBB_op_ctxt));
for(const auto& env3 : range) {
if( (ramBitCast<RamDomain>(env0[0]) != ramBitCast<RamDomain>(env3[0])) && (ramBitCast<RamDomain>(env2[0]) != ramBitCast<RamDomain>(env3[0])) && rel_5_MayPredecessorBBModuloThrow->contains(Tuple<RamDomain,2>{{ramBitCast(env3[0]),ramBitCast(env1[1])}},READ_OP_CONTEXT(rel_5_MayPredecessorBBModuloThrow_op_ctxt))) {
Tuple<RamDomain,2> tuple{{ramBitCast(env1[1]),ramBitCast(env0[1])}};
rel_13_new_BinaryExpressionBB->insert(tuple,READ_OP_CONTEXT(rel_13_new_BinaryExpressionBB_op_ctxt));
}
}
}
}
}
}
}
}
();}
if(rel_13_new_BinaryExpressionBB->empty()) break;
[&](){
CREATE_OP_CONTEXT(rel_11_BinaryExpressionBB_op_ctxt,rel_11_BinaryExpressionBB->createContext());
CREATE_OP_CONTEXT(rel_13_new_BinaryExpressionBB_op_ctxt,rel_13_new_BinaryExpressionBB->createContext());
for(const auto& env0 : *rel_13_new_BinaryExpressionBB) {
Tuple<RamDomain,2> tuple{{ramBitCast(env0[0]),ramBitCast(env0[1])}};
rel_11_BinaryExpressionBB->insert(tuple,READ_OP_CONTEXT(rel_11_BinaryExpressionBB_op_ctxt));
}
}
();std::swap(rel_12_delta_BinaryExpressionBB, rel_13_new_BinaryExpressionBB);
rel_13_new_BinaryExpressionBB->purge();
iter++;
}
iter = 0;
rel_12_delta_BinaryExpressionBB->purge();
rel_13_new_BinaryExpressionBB->purge();
if (performIO) {
try {std::map<std::string, std::string> directiveMap({{"IO","file"},{"attributeNames","?assign\t?exp"},{"auxArity","0"},{"name","BinaryExpressionBB"},{"operation","output"},{"output-dir","Results/AvailableExpressions/"},{"params","{\"records\": {\"BinExp\": {\"arity\": 3, \"params\": [\"?left\", \"?op\", \"?right\"]}}, \"relation\": {\"arity\": 2, \"params\": [\"?assign\", \"?exp\"]}}"},{"types","{\"ADTs\": {}, \"records\": {\"r:BinExp\": {\"arity\": 3, \"types\": [\"s:Var\", \"s:Operator\", \"s:Var\"]}}, \"relation\": {\"arity\": 2, \"types\": [\"s:Instruction\", \"r:BinExp\"]}}"}});
if (!outputDirectory.empty()) {directiveMap["output-dir"] = outputDirectory;}
IOSystem::getInstance().getWriter(directiveMap, symTable, recordTable)->writeAll(*rel_11_BinaryExpressionBB);
} catch (std::exception& e) {std::cerr << e.what();exit(1);}
}
if (performIO) rel_1_BasicBlockHead->purge();
if (performIO) rel_8_BinaryExpression->purge();
}
#ifdef _MSC_VER
#pragma warning(default: 4100)
#endif // _MSC_VER
#ifdef _MSC_VER
#pragma warning(disable: 4100)
#endif // _MSC_VER
void subroutine_3(const std::vector<RamDomain>& args, std::vector<RamDomain>& ret) {
signalHandler->setMsg(R"_(__agg_subclause(?BB2,?BB3,?exp) :- 
   BinaryExpressionBB(?BB2,?exp),
   MayPredecessorBBModuloThrow(?BB2,?BB3).
in file  [0:0-0:0])_");
if(!(rel_11_BinaryExpressionBB->empty()) && !(rel_5_MayPredecessorBBModuloThrow->empty())) {
[&](){
CREATE_OP_CONTEXT(rel_5_MayPredecessorBBModuloThrow_op_ctxt,rel_5_MayPredecessorBBModuloThrow->createContext());
CREATE_OP_CONTEXT(rel_11_BinaryExpressionBB_op_ctxt,rel_11_BinaryExpressionBB->createContext());
CREATE_OP_CONTEXT(rel_14_agg_subclause_op_ctxt,rel_14_agg_subclause->createContext());
for(const auto& env0 : *rel_11_BinaryExpressionBB) {
auto range = rel_5_MayPredecessorBBModuloThrow->lowerUpperRange_10(Tuple<RamDomain,2>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MIN_RAM_SIGNED)}},Tuple<RamDomain,2>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MAX_RAM_SIGNED)}},READ_OP_CONTEXT(rel_5_MayPredecessorBBModuloThrow_op_ctxt));
for(const auto& env1 : range) {
Tuple<RamDomain,3> tuple{{ramBitCast(env0[0]),ramBitCast(env1[1]),ramBitCast(env0[1])}};
rel_14_agg_subclause->insert(tuple,READ_OP_CONTEXT(rel_14_agg_subclause_op_ctxt));
}
}
}
();}
}
#ifdef _MSC_VER
#pragma warning(default: 4100)
#endif // _MSC_VER
#ifdef _MSC_VER
#pragma warning(disable: 4100)
#endif // _MSC_VER
void subroutine_4(const std::vector<RamDomain>& args, std::vector<RamDomain>& ret) {
signalHandler->setMsg(R"_(NoJoinExpressions(?BB3,?exp) :- 
   BinaryExpressionBB(?BB1,?exp),
   MayPredecessorBBModuloThrow(?BB1,?BB3),
   NrOfPredBB(?BB3,?a),
   ?a > 1,
   @generator_0 < ?a,
   @generator_0 = count : { __agg_subclause(+underscore_8,?BB3,?exp) }.
in file /home/kotname/Documents/10_Semester/INF_PM_ANW/doop/master/TestKnut/Analysis/AvailableExpressions.dl [121:1-127:13])_");
if(!(rel_5_MayPredecessorBBModuloThrow->empty()) && !(rel_10_NrOfPredBB->empty()) && !(rel_11_BinaryExpressionBB->empty())) {
[&](){
CREATE_OP_CONTEXT(rel_5_MayPredecessorBBModuloThrow_op_ctxt,rel_5_MayPredecessorBBModuloThrow->createContext());
CREATE_OP_CONTEXT(rel_10_NrOfPredBB_op_ctxt,rel_10_NrOfPredBB->createContext());
CREATE_OP_CONTEXT(rel_11_BinaryExpressionBB_op_ctxt,rel_11_BinaryExpressionBB->createContext());
CREATE_OP_CONTEXT(rel_14_agg_subclause_op_ctxt,rel_14_agg_subclause->createContext());
CREATE_OP_CONTEXT(rel_15_NoJoinExpressions_op_ctxt,rel_15_NoJoinExpressions->createContext());
for(const auto& env0 : *rel_11_BinaryExpressionBB) {
auto range = rel_5_MayPredecessorBBModuloThrow->lowerUpperRange_10(Tuple<RamDomain,2>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MIN_RAM_SIGNED)}},Tuple<RamDomain,2>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MAX_RAM_SIGNED)}},READ_OP_CONTEXT(rel_5_MayPredecessorBBModuloThrow_op_ctxt));
for(const auto& env1 : range) {
Tuple<RamDomain,1> env2;
bool shouldRunNested = false;
shouldRunNested = true;
RamSigned res0 = 0;
auto range = rel_14_agg_subclause->lowerUpperRange_011(Tuple<RamDomain,3>{{ramBitCast<RamDomain>(MIN_RAM_SIGNED), ramBitCast(env1[1]), ramBitCast(env0[1])}},Tuple<RamDomain,3>{{ramBitCast<RamDomain>(MAX_RAM_SIGNED), ramBitCast(env1[1]), ramBitCast(env0[1])}},READ_OP_CONTEXT(rel_14_agg_subclause_op_ctxt));
for(const auto& env2 : range) {
if( true) {
shouldRunNested = true;
++res0
;}
}
env2[0] = ramBitCast(res0);
if (shouldRunNested) {
if( (ramBitCast<RamDomain>(env2[0]) == ramBitCast<RamDomain>(env2[0]))) {
auto range = rel_10_NrOfPredBB->lowerUpperRange_12(Tuple<RamDomain,2>{{ramBitCast(env1[1]), ramBitCast(RamSigned(1))}},Tuple<RamDomain,2>{{ramBitCast(env1[1]), ramBitCast<RamDomain>(MAX_RAM_SIGNED)}},READ_OP_CONTEXT(rel_10_NrOfPredBB_op_ctxt));
for(const auto& env3 : range) {
if( (ramBitCast<RamDomain>(env3[1]) != ramBitCast<RamDomain>(RamSigned(1))) && (ramBitCast<RamSigned>(env2[0]) < ramBitCast<RamSigned>(env3[1]))) {
Tuple<RamDomain,2> tuple{{ramBitCast(env1[1]),ramBitCast(env0[1])}};
rel_15_NoJoinExpressions->insert(tuple,READ_OP_CONTEXT(rel_15_NoJoinExpressions_op_ctxt));
}
}
}
}
}
}
}
();}
if (performIO) {
try {std::map<std::string, std::string> directiveMap({{"IO","file"},{"attributeNames","?BB1\t?exp"},{"auxArity","0"},{"name","NoJoinExpressions"},{"operation","output"},{"output-dir","Results/AvailableExpressions/"},{"params","{\"records\": {\"BinExp\": {\"arity\": 3, \"params\": [\"?left\", \"?op\", \"?right\"]}}, \"relation\": {\"arity\": 2, \"params\": [\"?BB1\", \"?exp\"]}}"},{"types","{\"ADTs\": {}, \"records\": {\"r:BinExp\": {\"arity\": 3, \"types\": [\"s:Var\", \"s:Operator\", \"s:Var\"]}}, \"relation\": {\"arity\": 2, \"types\": [\"s:Instruction\", \"r:BinExp\"]}}"}});
if (!outputDirectory.empty()) {directiveMap["output-dir"] = outputDirectory;}
IOSystem::getInstance().getWriter(directiveMap, symTable, recordTable)->writeAll(*rel_15_NoJoinExpressions);
} catch (std::exception& e) {std::cerr << e.what();exit(1);}
}
if (performIO) rel_5_MayPredecessorBBModuloThrow->purge();
if (performIO) rel_11_BinaryExpressionBB->purge();
if (performIO) rel_10_NrOfPredBB->purge();
if (performIO) rel_14_agg_subclause->purge();
}
#ifdef _MSC_VER
#pragma warning(default: 4100)
#endif // _MSC_VER
#ifdef _MSC_VER
#pragma warning(disable: 4100)
#endif // _MSC_VER
void subroutine_5(const std::vector<RamDomain>& args, std::vector<RamDomain>& ret) {
if (performIO) {
try {std::map<std::string, std::string> directiveMap({{"IO","file"},{"attributeNames","?to1\t?to2"},{"auxArity","0"},{"name","CommonSubExpression"},{"operation","output"},{"output-dir","Results/AvailableExpressions/"},{"params","{\"records\": {\"BinExp\": {\"arity\": 3, \"params\": [\"?left\", \"?op\", \"?right\"]}}, \"relation\": {\"arity\": 2, \"params\": [\"?to1\", \"?to2\"]}}"},{"types","{\"ADTs\": {}, \"records\": {\"r:BinExp\": {\"arity\": 3, \"types\": [\"s:Var\", \"s:Operator\", \"s:Var\"]}}, \"relation\": {\"arity\": 2, \"types\": [\"s:Var\", \"s:Var\"]}}"}});
if (!outputDirectory.empty()) {directiveMap["output-dir"] = outputDirectory;}
IOSystem::getInstance().getWriter(directiveMap, symTable, recordTable)->writeAll(*rel_16_CommonSubExpression);
} catch (std::exception& e) {std::cerr << e.what();exit(1);}
}
}
#ifdef _MSC_VER
#pragma warning(default: 4100)
#endif // _MSC_VER
#ifdef _MSC_VER
#pragma warning(disable: 4100)
#endif // _MSC_VER
void subroutine_6(const std::vector<RamDomain>& args, std::vector<RamDomain>& ret) {
if (performIO) {
try {std::map<std::string, std::string> directiveMap({{"IO","file"},{"attributeNames","?assign\t?left\t?op\t?to"},{"auxArity","0"},{"name","UnaryExpression"},{"operation","output"},{"output-dir","Results/AvailableExpressions/"},{"params","{\"records\": {\"BinExp\": {\"arity\": 3, \"params\": [\"?left\", \"?op\", \"?right\"]}}, \"relation\": {\"arity\": 4, \"params\": [\"?assign\", \"?left\", \"?op\", \"?to\"]}}"},{"types","{\"ADTs\": {}, \"records\": {\"r:BinExp\": {\"arity\": 3, \"types\": [\"s:Var\", \"s:Operator\", \"s:Var\"]}}, \"relation\": {\"arity\": 4, \"types\": [\"s:Instruction\", \"s:Var\", \"s:Operator\", \"s:Var\"]}}"}});
if (!outputDirectory.empty()) {directiveMap["output-dir"] = outputDirectory;}
IOSystem::getInstance().getWriter(directiveMap, symTable, recordTable)->writeAll(*rel_17_UnaryExpression);
} catch (std::exception& e) {std::cerr << e.what();exit(1);}
}
}
#ifdef _MSC_VER
#pragma warning(default: 4100)
#endif // _MSC_VER
#ifdef _MSC_VER
#pragma warning(disable: 4100)
#endif // _MSC_VER
void subroutine_7(const std::vector<RamDomain>& args, std::vector<RamDomain>& ret) {
if (performIO) {
try {std::map<std::string, std::string> directiveMap({{"IO","file"},{"attributeNames","?assign\t?op"},{"auxArity","0"},{"delimter","\t"},{"fact-dir","../out/16AvExpr/database"},{"filename","OperatorAt.facts"},{"name","OperatorAt"},{"operation","input"},{"params","{\"records\": {\"BinExp\": {\"arity\": 3, \"params\": [\"?left\", \"?op\", \"?right\"]}}, \"relation\": {\"arity\": 2, \"params\": [\"?assign\", \"?op\"]}}"},{"types","{\"ADTs\": {}, \"records\": {\"r:BinExp\": {\"arity\": 3, \"types\": [\"s:Var\", \"s:Operator\", \"s:Var\"]}}, \"relation\": {\"arity\": 2, \"types\": [\"s:Instruction\", \"s:Operator\"]}}"}});
if (!inputDirectory.empty()) {directiveMap["fact-dir"] = inputDirectory;}
IOSystem::getInstance().getReader(directiveMap, symTable, recordTable)->readAll(*rel_3_OperatorAt);
} catch (std::exception& e) {std::cerr << "Error loading data: " << e.what() << '\n';}
}
}
#ifdef _MSC_VER
#pragma warning(default: 4100)
#endif // _MSC_VER
#ifdef _MSC_VER
#pragma warning(disable: 4100)
#endif // _MSC_VER
void subroutine_8(const std::vector<RamDomain>& args, std::vector<RamDomain>& ret) {
if (performIO) {
try {std::map<std::string, std::string> directiveMap({{"IO","file"},{"attributeNames","?ifNode\t?lineNr\t?jump\t?method"},{"auxArity","0"},{"delimiter","\t"},{"fact-dir","../out/16AvExpr/database"},{"filename","If.facts"},{"name","If"},{"operation","input"},{"params","{\"records\": {\"BinExp\": {\"arity\": 3, \"params\": [\"?left\", \"?op\", \"?right\"]}}, \"relation\": {\"arity\": 4, \"params\": [\"?ifNode\", \"?lineNr\", \"?jump\", \"?method\"]}}"},{"types","{\"ADTs\": {}, \"records\": {\"r:BinExp\": {\"arity\": 3, \"types\": [\"s:Var\", \"s:Operator\", \"s:Var\"]}}, \"relation\": {\"arity\": 4, \"types\": [\"s:Instruction\", \"i:number\", \"i:number\", \"s:Method\"]}}"}});
if (!inputDirectory.empty()) {directiveMap["fact-dir"] = inputDirectory;}
IOSystem::getInstance().getReader(directiveMap, symTable, recordTable)->readAll(*rel_4_If);
} catch (std::exception& e) {std::cerr << "Error loading data: " << e.what() << '\n';}
}
}
#ifdef _MSC_VER
#pragma warning(default: 4100)
#endif // _MSC_VER
#ifdef _MSC_VER
#pragma warning(disable: 4100)
#endif // _MSC_VER
void subroutine_9(const std::vector<RamDomain>& args, std::vector<RamDomain>& ret) {
if (performIO) {
try {std::map<std::string, std::string> directiveMap({{"IO","file"},{"attributeNames","?inst\t?inst1"},{"auxArity","0"},{"delimiter","\t"},{"fact-dir","../out/16AvExpr/database"},{"filename","MayPredecessorBBModuloThrow.csv"},{"name","MayPredecessorBBModuloThrow"},{"operation","input"},{"params","{\"records\": {\"BinExp\": {\"arity\": 3, \"params\": [\"?left\", \"?op\", \"?right\"]}}, \"relation\": {\"arity\": 2, \"params\": [\"?inst\", \"?inst1\"]}}"},{"types","{\"ADTs\": {}, \"records\": {\"r:BinExp\": {\"arity\": 3, \"types\": [\"s:Var\", \"s:Operator\", \"s:Var\"]}}, \"relation\": {\"arity\": 2, \"types\": [\"s:Instruction\", \"s:Instruction\"]}}"}});
if (!inputDirectory.empty()) {directiveMap["fact-dir"] = inputDirectory;}
IOSystem::getInstance().getReader(directiveMap, symTable, recordTable)->readAll(*rel_5_MayPredecessorBBModuloThrow);
} catch (std::exception& e) {std::cerr << "Error loading data: " << e.what() << '\n';}
}
}
#ifdef _MSC_VER
#pragma warning(default: 4100)
#endif // _MSC_VER
#ifdef _MSC_VER
#pragma warning(disable: 4100)
#endif // _MSC_VER
void subroutine_10(const std::vector<RamDomain>& args, std::vector<RamDomain>& ret) {
if (performIO) {
try {std::map<std::string, std::string> directiveMap({{"IO","file"},{"attributeNames","?instruction\t?pos\t?from"},{"auxArity","0"},{"delimiter","\t"},{"fact-dir","../out/16AvExpr/database"},{"filename","AssignOperFrom.facts"},{"name","AssignOperFrom"},{"operation","input"},{"params","{\"records\": {\"BinExp\": {\"arity\": 3, \"params\": [\"?left\", \"?op\", \"?right\"]}}, \"relation\": {\"arity\": 3, \"params\": [\"?instruction\", \"?pos\", \"?from\"]}}"},{"types","{\"ADTs\": {}, \"records\": {\"r:BinExp\": {\"arity\": 3, \"types\": [\"s:Var\", \"s:Operator\", \"s:Var\"]}}, \"relation\": {\"arity\": 3, \"types\": [\"s:Instruction\", \"i:number\", \"s:Var\"]}}"}});
if (!inputDirectory.empty()) {directiveMap["fact-dir"] = inputDirectory;}
IOSystem::getInstance().getReader(directiveMap, symTable, recordTable)->readAll(*rel_6_AssignOperFrom);
} catch (std::exception& e) {std::cerr << "Error loading data: " << e.what() << '\n';}
}
}
#ifdef _MSC_VER
#pragma warning(default: 4100)
#endif // _MSC_VER
#ifdef _MSC_VER
#pragma warning(disable: 4100)
#endif // _MSC_VER
void subroutine_11(const std::vector<RamDomain>& args, std::vector<RamDomain>& ret) {
if (performIO) {
try {std::map<std::string, std::string> directiveMap({{"IO","file"},{"attributeNames","?instruction\t?pos\t?from"},{"auxArity","0"},{"delimiter","\t"},{"fact-dir","../out/16AvExpr/database"},{"filename","AssignOperFromConstant.facts"},{"name","AssignOperFromConstant"},{"operation","input"},{"params","{\"records\": {\"BinExp\": {\"arity\": 3, \"params\": [\"?left\", \"?op\", \"?right\"]}}, \"relation\": {\"arity\": 3, \"params\": [\"?instruction\", \"?pos\", \"?from\"]}}"},{"types","{\"ADTs\": {}, \"records\": {\"r:BinExp\": {\"arity\": 3, \"types\": [\"s:Var\", \"s:Operator\", \"s:Var\"]}}, \"relation\": {\"arity\": 3, \"types\": [\"s:Instruction\", \"i:number\", \"i:number\"]}}"}});
if (!inputDirectory.empty()) {directiveMap["fact-dir"] = inputDirectory;}
IOSystem::getInstance().getReader(directiveMap, symTable, recordTable)->readAll(*rel_7_AssignOperFromConstant);
} catch (std::exception& e) {std::cerr << "Error loading data: " << e.what() << '\n';}
}
}
#ifdef _MSC_VER
#pragma warning(default: 4100)
#endif // _MSC_VER
#ifdef _MSC_VER
#pragma warning(disable: 4100)
#endif // _MSC_VER
void subroutine_12(const std::vector<RamDomain>& args, std::vector<RamDomain>& ret) {
signalHandler->setMsg(R"_(BinaryExpression(?assign,[?left,?op,?right],?to) :- 
   OperatorAt(?assign,?op),
   !If(?assign,_,_,_),
   AssignBinop(?assign,_,?to,_),
   AssignOperFrom(?assign,?pos1,?left),
   AssignOperFrom(?assign,?pos2,?right),
   ?pos1 < ?pos2.
in file /home/kotname/Documents/10_Semester/INF_PM_ANW/doop/master/TestKnut/Analysis/AvailableExpressions.dl [66:1-72:19])_");
if(!(rel_3_OperatorAt->empty()) && !(rel_2_AssignBinop->empty()) && !(rel_6_AssignOperFrom->empty())) {
[&](){
CREATE_OP_CONTEXT(rel_6_AssignOperFrom_op_ctxt,rel_6_AssignOperFrom->createContext());
CREATE_OP_CONTEXT(rel_3_OperatorAt_op_ctxt,rel_3_OperatorAt->createContext());
CREATE_OP_CONTEXT(rel_2_AssignBinop_op_ctxt,rel_2_AssignBinop->createContext());
CREATE_OP_CONTEXT(rel_4_If_op_ctxt,rel_4_If->createContext());
CREATE_OP_CONTEXT(rel_8_BinaryExpression_op_ctxt,rel_8_BinaryExpression->createContext());
for(const auto& env0 : *rel_3_OperatorAt) {
if( !(!rel_4_If->lowerUpperRange_1000(Tuple<RamDomain,4>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MIN_RAM_SIGNED), ramBitCast<RamDomain>(MIN_RAM_SIGNED), ramBitCast<RamDomain>(MIN_RAM_SIGNED)}},Tuple<RamDomain,4>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MAX_RAM_SIGNED), ramBitCast<RamDomain>(MAX_RAM_SIGNED), ramBitCast<RamDomain>(MAX_RAM_SIGNED)}},READ_OP_CONTEXT(rel_4_If_op_ctxt)).empty())) {
auto range = rel_2_AssignBinop->lowerUpperRange_1000(Tuple<RamDomain,4>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MIN_RAM_SIGNED), ramBitCast<RamDomain>(MIN_RAM_SIGNED), ramBitCast<RamDomain>(MIN_RAM_SIGNED)}},Tuple<RamDomain,4>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MAX_RAM_SIGNED), ramBitCast<RamDomain>(MAX_RAM_SIGNED), ramBitCast<RamDomain>(MAX_RAM_SIGNED)}},READ_OP_CONTEXT(rel_2_AssignBinop_op_ctxt));
for(const auto& env1 : range) {
auto range = rel_6_AssignOperFrom->lowerUpperRange_100(Tuple<RamDomain,3>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MIN_RAM_SIGNED), ramBitCast<RamDomain>(MIN_RAM_SIGNED)}},Tuple<RamDomain,3>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MAX_RAM_SIGNED), ramBitCast<RamDomain>(MAX_RAM_SIGNED)}},READ_OP_CONTEXT(rel_6_AssignOperFrom_op_ctxt));
for(const auto& env2 : range) {
auto range = rel_6_AssignOperFrom->lowerUpperRange_120(Tuple<RamDomain,3>{{ramBitCast(env0[0]), ramBitCast(env2[1]), ramBitCast<RamDomain>(MIN_RAM_SIGNED)}},Tuple<RamDomain,3>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MAX_RAM_SIGNED), ramBitCast<RamDomain>(MAX_RAM_SIGNED)}},READ_OP_CONTEXT(rel_6_AssignOperFrom_op_ctxt));
for(const auto& env3 : range) {
if( (ramBitCast<RamDomain>(env2[1]) != ramBitCast<RamDomain>(env3[1]))) {
Tuple<RamDomain,3> tuple{{ramBitCast(env0[0]),ramBitCast(pack(recordTable,Tuple<RamDomain,3>{{ramBitCast(ramBitCast(env2[2])),ramBitCast(ramBitCast(env0[1])),ramBitCast(ramBitCast(env3[2]))}}
)),ramBitCast(env1[2])}};
rel_8_BinaryExpression->insert(tuple,READ_OP_CONTEXT(rel_8_BinaryExpression_op_ctxt));
}
}
}
}
}
}
}
();}
signalHandler->setMsg(R"_(BinaryExpression(?assign,[?left,?op,to_string(?right)],?to) :- 
   OperatorAt(?assign,?op),
   !If(?assign,_,_,_),
   AssignBinop(?assign,_,?to,_),
   AssignOperFrom(?assign,?pos1,?left),
   AssignOperFromConstant(?assign,?pos2,?right),
   ?pos1 < ?pos2.
in file /home/kotname/Documents/10_Semester/INF_PM_ANW/doop/master/TestKnut/Analysis/AvailableExpressions.dl [75:1-81:19])_");
if(!(rel_2_AssignBinop->empty()) && !(rel_6_AssignOperFrom->empty()) && !(rel_3_OperatorAt->empty()) && !(rel_7_AssignOperFromConstant->empty())) {
[&](){
CREATE_OP_CONTEXT(rel_6_AssignOperFrom_op_ctxt,rel_6_AssignOperFrom->createContext());
CREATE_OP_CONTEXT(rel_3_OperatorAt_op_ctxt,rel_3_OperatorAt->createContext());
CREATE_OP_CONTEXT(rel_2_AssignBinop_op_ctxt,rel_2_AssignBinop->createContext());
CREATE_OP_CONTEXT(rel_4_If_op_ctxt,rel_4_If->createContext());
CREATE_OP_CONTEXT(rel_7_AssignOperFromConstant_op_ctxt,rel_7_AssignOperFromConstant->createContext());
CREATE_OP_CONTEXT(rel_8_BinaryExpression_op_ctxt,rel_8_BinaryExpression->createContext());
for(const auto& env0 : *rel_3_OperatorAt) {
if( !(!rel_4_If->lowerUpperRange_1000(Tuple<RamDomain,4>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MIN_RAM_SIGNED), ramBitCast<RamDomain>(MIN_RAM_SIGNED), ramBitCast<RamDomain>(MIN_RAM_SIGNED)}},Tuple<RamDomain,4>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MAX_RAM_SIGNED), ramBitCast<RamDomain>(MAX_RAM_SIGNED), ramBitCast<RamDomain>(MAX_RAM_SIGNED)}},READ_OP_CONTEXT(rel_4_If_op_ctxt)).empty())) {
auto range = rel_2_AssignBinop->lowerUpperRange_1000(Tuple<RamDomain,4>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MIN_RAM_SIGNED), ramBitCast<RamDomain>(MIN_RAM_SIGNED), ramBitCast<RamDomain>(MIN_RAM_SIGNED)}},Tuple<RamDomain,4>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MAX_RAM_SIGNED), ramBitCast<RamDomain>(MAX_RAM_SIGNED), ramBitCast<RamDomain>(MAX_RAM_SIGNED)}},READ_OP_CONTEXT(rel_2_AssignBinop_op_ctxt));
for(const auto& env1 : range) {
auto range = rel_6_AssignOperFrom->lowerUpperRange_100(Tuple<RamDomain,3>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MIN_RAM_SIGNED), ramBitCast<RamDomain>(MIN_RAM_SIGNED)}},Tuple<RamDomain,3>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MAX_RAM_SIGNED), ramBitCast<RamDomain>(MAX_RAM_SIGNED)}},READ_OP_CONTEXT(rel_6_AssignOperFrom_op_ctxt));
for(const auto& env2 : range) {
auto range = rel_7_AssignOperFromConstant->lowerUpperRange_120(Tuple<RamDomain,3>{{ramBitCast(env0[0]), ramBitCast(env2[1]), ramBitCast<RamDomain>(MIN_RAM_SIGNED)}},Tuple<RamDomain,3>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MAX_RAM_SIGNED), ramBitCast<RamDomain>(MAX_RAM_SIGNED)}},READ_OP_CONTEXT(rel_7_AssignOperFromConstant_op_ctxt));
for(const auto& env3 : range) {
if( (ramBitCast<RamDomain>(env2[1]) != ramBitCast<RamDomain>(env3[1]))) {
Tuple<RamDomain,3> tuple{{ramBitCast(env0[0]),ramBitCast(pack(recordTable,Tuple<RamDomain,3>{{ramBitCast(ramBitCast(env2[2])),ramBitCast(ramBitCast(env0[1])),ramBitCast(ramBitCast(symTable.encode(std::to_string(env3[2]))))}}
)),ramBitCast(env1[2])}};
rel_8_BinaryExpression->insert(tuple,READ_OP_CONTEXT(rel_8_BinaryExpression_op_ctxt));
}
}
}
}
}
}
}
();}
signalHandler->setMsg(R"_(BinaryExpression(?assign,[to_string(?left),?op,?right],?to) :- 
   OperatorAt(?assign,?op),
   !If(?assign,_,_,_),
   AssignBinop(?assign,_,?to,_),
   AssignOperFromConstant(?assign,?pos1,?left),
   AssignOperFrom(?assign,?pos2,?right),
   ?pos1 < ?pos2.
in file /home/kotname/Documents/10_Semester/INF_PM_ANW/doop/master/TestKnut/Analysis/AvailableExpressions.dl [83:1-89:19])_");
if(!(rel_2_AssignBinop->empty()) && !(rel_7_AssignOperFromConstant->empty()) && !(rel_3_OperatorAt->empty()) && !(rel_6_AssignOperFrom->empty())) {
[&](){
CREATE_OP_CONTEXT(rel_6_AssignOperFrom_op_ctxt,rel_6_AssignOperFrom->createContext());
CREATE_OP_CONTEXT(rel_3_OperatorAt_op_ctxt,rel_3_OperatorAt->createContext());
CREATE_OP_CONTEXT(rel_2_AssignBinop_op_ctxt,rel_2_AssignBinop->createContext());
CREATE_OP_CONTEXT(rel_4_If_op_ctxt,rel_4_If->createContext());
CREATE_OP_CONTEXT(rel_7_AssignOperFromConstant_op_ctxt,rel_7_AssignOperFromConstant->createContext());
CREATE_OP_CONTEXT(rel_8_BinaryExpression_op_ctxt,rel_8_BinaryExpression->createContext());
for(const auto& env0 : *rel_3_OperatorAt) {
if( !(!rel_4_If->lowerUpperRange_1000(Tuple<RamDomain,4>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MIN_RAM_SIGNED), ramBitCast<RamDomain>(MIN_RAM_SIGNED), ramBitCast<RamDomain>(MIN_RAM_SIGNED)}},Tuple<RamDomain,4>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MAX_RAM_SIGNED), ramBitCast<RamDomain>(MAX_RAM_SIGNED), ramBitCast<RamDomain>(MAX_RAM_SIGNED)}},READ_OP_CONTEXT(rel_4_If_op_ctxt)).empty())) {
auto range = rel_2_AssignBinop->lowerUpperRange_1000(Tuple<RamDomain,4>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MIN_RAM_SIGNED), ramBitCast<RamDomain>(MIN_RAM_SIGNED), ramBitCast<RamDomain>(MIN_RAM_SIGNED)}},Tuple<RamDomain,4>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MAX_RAM_SIGNED), ramBitCast<RamDomain>(MAX_RAM_SIGNED), ramBitCast<RamDomain>(MAX_RAM_SIGNED)}},READ_OP_CONTEXT(rel_2_AssignBinop_op_ctxt));
for(const auto& env1 : range) {
auto range = rel_7_AssignOperFromConstant->lowerUpperRange_100(Tuple<RamDomain,3>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MIN_RAM_SIGNED), ramBitCast<RamDomain>(MIN_RAM_SIGNED)}},Tuple<RamDomain,3>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MAX_RAM_SIGNED), ramBitCast<RamDomain>(MAX_RAM_SIGNED)}},READ_OP_CONTEXT(rel_7_AssignOperFromConstant_op_ctxt));
for(const auto& env2 : range) {
auto range = rel_6_AssignOperFrom->lowerUpperRange_120(Tuple<RamDomain,3>{{ramBitCast(env0[0]), ramBitCast(env2[1]), ramBitCast<RamDomain>(MIN_RAM_SIGNED)}},Tuple<RamDomain,3>{{ramBitCast(env0[0]), ramBitCast<RamDomain>(MAX_RAM_SIGNED), ramBitCast<RamDomain>(MAX_RAM_SIGNED)}},READ_OP_CONTEXT(rel_6_AssignOperFrom_op_ctxt));
for(const auto& env3 : range) {
if( (ramBitCast<RamDomain>(env2[1]) != ramBitCast<RamDomain>(env3[1]))) {
Tuple<RamDomain,3> tuple{{ramBitCast(env0[0]),ramBitCast(pack(recordTable,Tuple<RamDomain,3>{{ramBitCast(ramBitCast(symTable.encode(std::to_string(env2[2])))),ramBitCast(ramBitCast(env0[1])),ramBitCast(ramBitCast(env3[2]))}}
)),ramBitCast(env1[2])}};
rel_8_BinaryExpression->insert(tuple,READ_OP_CONTEXT(rel_8_BinaryExpression_op_ctxt));
}
}
}
}
}
}
}
();}
if (performIO) {
try {std::map<std::string, std::string> directiveMap({{"IO","file"},{"attributeNames","?assign\t?b\t?to"},{"auxArity","0"},{"name","BinaryExpression"},{"operation","output"},{"output-dir","Results/AvailableExpressions/"},{"params","{\"records\": {\"BinExp\": {\"arity\": 3, \"params\": [\"?left\", \"?op\", \"?right\"]}}, \"relation\": {\"arity\": 3, \"params\": [\"?assign\", \"?b\", \"?to\"]}}"},{"types","{\"ADTs\": {}, \"records\": {\"r:BinExp\": {\"arity\": 3, \"types\": [\"s:Var\", \"s:Operator\", \"s:Var\"]}}, \"relation\": {\"arity\": 3, \"types\": [\"s:Instruction\", \"r:BinExp\", \"s:Var\"]}}"}});
if (!outputDirectory.empty()) {directiveMap["output-dir"] = outputDirectory;}
IOSystem::getInstance().getWriter(directiveMap, symTable, recordTable)->writeAll(*rel_8_BinaryExpression);
} catch (std::exception& e) {std::cerr << e.what();exit(1);}
}
if (performIO) rel_2_AssignBinop->purge();
if (performIO) rel_3_OperatorAt->purge();
if (performIO) rel_4_If->purge();
if (performIO) rel_6_AssignOperFrom->purge();
if (performIO) rel_7_AssignOperFromConstant->purge();
}
#ifdef _MSC_VER
#pragma warning(default: 4100)
#endif // _MSC_VER
#ifdef _MSC_VER
#pragma warning(disable: 4100)
#endif // _MSC_VER
void subroutine_13(const std::vector<RamDomain>& args, std::vector<RamDomain>& ret) {
if (performIO) {
try {std::map<std::string, std::string> directiveMap({{"IO","file"},{"attributeNames","?ass"},{"auxArity","0"},{"delimiter","\t"},{"fact-dir","../out/16AvExpr/database"},{"filename","BasicBlockBegin.csv"},{"name","BasicBlockBegin"},{"operation","input"},{"params","{\"records\": {\"BinExp\": {\"arity\": 3, \"params\": [\"?left\", \"?op\", \"?right\"]}}, \"relation\": {\"arity\": 1, \"params\": [\"?ass\"]}}"},{"types","{\"ADTs\": {}, \"records\": {\"r:BinExp\": {\"arity\": 3, \"types\": [\"s:Var\", \"s:Operator\", \"s:Var\"]}}, \"relation\": {\"arity\": 1, \"types\": [\"s:Instruction\"]}}"}});
if (!inputDirectory.empty()) {directiveMap["fact-dir"] = inputDirectory;}
IOSystem::getInstance().getReader(directiveMap, symTable, recordTable)->readAll(*rel_9_BasicBlockBegin);
} catch (std::exception& e) {std::cerr << "Error loading data: " << e.what() << '\n';}
}
}
#ifdef _MSC_VER
#pragma warning(default: 4100)
#endif // _MSC_VER
#ifdef _MSC_VER
#pragma warning(disable: 4100)
#endif // _MSC_VER
void subroutine_14(const std::vector<RamDomain>& args, std::vector<RamDomain>& ret) {
signalHandler->setMsg(R"_(NrOfPredBB(?BB1,@generator_0) :- 
   BasicBlockBegin(?BB1),
   @generator_0 = count : { MayPredecessorBBModuloThrow(+underscore_7,?BB1) }.
in file /home/kotname/Documents/10_Semester/INF_PM_ANW/doop/master/TestKnut/Analysis/AvailableExpressions.dl [60:1-63:57])_");
if(!(rel_9_BasicBlockBegin->empty())) {
[&](){
CREATE_OP_CONTEXT(rel_5_MayPredecessorBBModuloThrow_op_ctxt,rel_5_MayPredecessorBBModuloThrow->createContext());
CREATE_OP_CONTEXT(rel_9_BasicBlockBegin_op_ctxt,rel_9_BasicBlockBegin->createContext());
CREATE_OP_CONTEXT(rel_10_NrOfPredBB_op_ctxt,rel_10_NrOfPredBB->createContext());
for(const auto& env0 : *rel_9_BasicBlockBegin) {
Tuple<RamDomain,1> env1;
bool shouldRunNested = false;
shouldRunNested = true;
RamSigned res0 = 0;
auto range = rel_5_MayPredecessorBBModuloThrow->lowerUpperRange_01(Tuple<RamDomain,2>{{ramBitCast<RamDomain>(MIN_RAM_SIGNED), ramBitCast(env0[0])}},Tuple<RamDomain,2>{{ramBitCast<RamDomain>(MAX_RAM_SIGNED), ramBitCast(env0[0])}},READ_OP_CONTEXT(rel_5_MayPredecessorBBModuloThrow_op_ctxt));
for(const auto& env1 : range) {
if( true) {
shouldRunNested = true;
++res0
;}
}
env1[0] = ramBitCast(res0);
if (shouldRunNested) {
if( (ramBitCast<RamDomain>(env1[0]) == ramBitCast<RamDomain>(env1[0]))) {
Tuple<RamDomain,2> tuple{{ramBitCast(env0[0]),ramBitCast(env1[0])}};
rel_10_NrOfPredBB->insert(tuple,READ_OP_CONTEXT(rel_10_NrOfPredBB_op_ctxt));
}
}
}
}
();}
if (performIO) {
try {std::map<std::string, std::string> directiveMap({{"IO","file"},{"attributeNames","?BB2\t?n"},{"auxArity","0"},{"name","NrOfPredBB"},{"operation","output"},{"output-dir","Results/AvailableExpressions/"},{"params","{\"records\": {\"BinExp\": {\"arity\": 3, \"params\": [\"?left\", \"?op\", \"?right\"]}}, \"relation\": {\"arity\": 2, \"params\": [\"?BB2\", \"?n\"]}}"},{"types","{\"ADTs\": {}, \"records\": {\"r:BinExp\": {\"arity\": 3, \"types\": [\"s:Var\", \"s:Operator\", \"s:Var\"]}}, \"relation\": {\"arity\": 2, \"types\": [\"s:Instruction\", \"i:number\"]}}"}});
if (!outputDirectory.empty()) {directiveMap["output-dir"] = outputDirectory;}
IOSystem::getInstance().getWriter(directiveMap, symTable, recordTable)->writeAll(*rel_10_NrOfPredBB);
} catch (std::exception& e) {std::cerr << e.what();exit(1);}
}
if (performIO) rel_9_BasicBlockBegin->purge();
}
#ifdef _MSC_VER
#pragma warning(default: 4100)
#endif // _MSC_VER
};
SouffleProgram *newInstance_AvailableExpressions(){return new Sf_AvailableExpressions;}
SymbolTable *getST_AvailableExpressions(SouffleProgram *p){return &reinterpret_cast<Sf_AvailableExpressions*>(p)->getSymbolTable();}

#ifdef __EMBEDDED_SOUFFLE__
class factory_Sf_AvailableExpressions: public souffle::ProgramFactory {
SouffleProgram *newInstance() {
return new Sf_AvailableExpressions();
};
public:
factory_Sf_AvailableExpressions() : ProgramFactory("AvailableExpressions"){}
};
extern "C" {
factory_Sf_AvailableExpressions __factory_Sf_AvailableExpressions_instance;
}
}
#else
}
int main(int argc, char** argv)
{
try{
souffle::CmdOptions opt(R"(Analysis/AvailableExpressions.dl)",
R"()",
R"()",
false,
R"()",
1);
if (!opt.parse(argc,argv)) return 1;
souffle::Sf_AvailableExpressions obj;
#if defined(_OPENMP) 
obj.setNumThreads(opt.getNumJobs());

#endif
obj.runAll(opt.getInputFileDir(), opt.getOutputFileDir());
return 0;
} catch(std::exception &e) { souffle::SignalHandler::instance()->error(e.what());}
}

#endif
