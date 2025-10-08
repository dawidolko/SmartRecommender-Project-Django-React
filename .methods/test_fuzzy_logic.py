#!/usr/bin/env python3
"""
Test script for Fuzzy Logic System
Demonstrates membership functions, fuzzification, and inference process.
"""

import sys
sys.path.append('../backend')

from home.custom_recommendation_engine import CustomFuzzySearch

def test_membership_functions():
    """Test membership function calculations"""
    print("=" * 60)
    print("TEST 1: Membership Functions")
    print("=" * 60)
    
    fuzzy_search = CustomFuzzySearch()
    
    # Test triangular membership function
    print("\n📐 Triangular MF (trimf):")
    print("   medium = trimf(0.2, 0.5, 0.7)")
    test_values = [0.1, 0.35, 0.5, 0.6, 0.8]
    
    for val in test_values:
        membership = fuzzy_search._membership_function(val, "trimf", [0.2, 0.5, 0.7])
        print(f"   μ_medium({val:.2f}) = {membership:.3f}")
    
    # Test trapezoidal membership function
    print("\n📐 Trapezoidal MF (trapmf):")
    print("   very_high = trapmf(0.7, 0.85, 1.0, 1.0)")
    
    for val in test_values:
        membership = fuzzy_search._membership_function(val, "trapmf", [0.7, 0.85, 1.0, 1.0])
        print(f"   μ_very_high({val:.2f}) = {membership:.3f}")

def test_fuzzification():
    """Test fuzzification process"""
    print("\n" + "=" * 60)
    print("TEST 2: Fuzzification (Crisp → Fuzzy)")
    print("=" * 60)
    
    fuzzy_search = CustomFuzzySearch()
    
    crisp_value = 0.75
    print(f"\n🔢 Input: name_match = {crisp_value}")
    print("   Converting to fuzzy set...")
    
    fuzzy_set = fuzzy_search._fuzzify(crisp_value, fuzzy_search.name_match_mf)
    
    print("\n   Membership degrees:")
    for term, membership in fuzzy_set.items():
        bar = "█" * int(membership * 20)
        print(f"   {term:12s}: {membership:.3f} {bar}")

def test_fuzzy_inference():
    """Test complete fuzzy inference system"""
    print("\n" + "=" * 60)
    print("TEST 3: Complete Fuzzy Inference (Mamdani)")
    print("=" * 60)
    
    fuzzy_search = CustomFuzzySearch()
    
    # Test case 1: High name match + excellent category
    print("\n🔍 Test Case 1: Gaming laptop search")
    name_score = 0.85
    category_score = 0.90
    price_score = 0.80
    
    print(f"   Inputs:")
    print(f"     - name_match: {name_score}")
    print(f"     - category_match: {category_score}")
    print(f"     - price_suitability: {price_score}")
    
    relevance = fuzzy_search.fuzzy_inference(name_score, category_score, price_score)
    
    print(f"\n   📊 Fuzzy Inference Output:")
    print(f"     → Relevance Score: {relevance:.3f} ({relevance*100:.1f}%)")
    
    # Test case 2: Medium name match + poor category
    print("\n🔍 Test Case 2: Weak match")
    name_score = 0.45
    category_score = 0.20
    price_score = 0.60
    
    print(f"   Inputs:")
    print(f"     - name_match: {name_score}")
    print(f"     - category_match: {category_score}")
    print(f"     - price_suitability: {price_score}")
    
    relevance = fuzzy_search.fuzzy_inference(name_score, category_score, price_score)
    
    print(f"\n   📊 Fuzzy Inference Output:")
    print(f"     → Relevance Score: {relevance:.3f} ({relevance*100:.1f}%)")
    
    # Test case 3: Perfect match
    print("\n🔍 Test Case 3: Perfect match")
    name_score = 1.0
    category_score = 1.0
    price_score = 1.0
    
    print(f"   Inputs:")
    print(f"     - name_match: {name_score}")
    print(f"     - category_match: {category_score}")
    print(f"     - price_suitability: {price_score}")
    
    relevance = fuzzy_search.fuzzy_inference(name_score, category_score, price_score)
    
    print(f"\n   📊 Fuzzy Inference Output:")
    print(f"     → Relevance Score: {relevance:.3f} ({relevance*100:.1f}%)")

def test_comparison():
    """Compare fuzzy logic vs traditional weighted sum"""
    print("\n" + "=" * 60)
    print("TEST 4: Fuzzy Logic vs Traditional Weighted Sum")
    print("=" * 60)
    
    fuzzy_search = CustomFuzzySearch()
    
    name_score = 0.85
    category_score = 0.90
    desc_score = 0.65
    spec_score = 0.40
    
    # Traditional approach
    traditional_score = (
        name_score * 0.45 +
        desc_score * 0.25 +
        category_score * 0.20 +
        spec_score * 0.10
    )
    
    # Fuzzy logic approach
    fuzzy_relevance = fuzzy_search.fuzzy_inference(name_score, category_score, 0.80)
    fuzzy_combined = (
        fuzzy_relevance * 0.70 +
        desc_score * 0.15 +
        spec_score * 0.10 +
        0.0 * 0.05  # tags
    )
    
    print(f"\n   Inputs:")
    print(f"     - name_match: {name_score}")
    print(f"     - category_match: {category_score}")
    print(f"     - desc_match: {desc_score}")
    print(f"     - spec_match: {spec_score}")
    
    print(f"\n   📊 Traditional Weighted Sum:")
    print(f"     = (0.85×0.45) + (0.65×0.25) + (0.90×0.20) + (0.40×0.10)")
    print(f"     = {traditional_score:.3f} ({traditional_score*100:.1f}%)")
    
    print(f"\n   🧠 Fuzzy Logic Inference:")
    print(f"     Fuzzy relevance: {fuzzy_relevance:.3f}")
    print(f"     Combined score: {fuzzy_combined:.3f} ({fuzzy_combined*100:.1f}%)")
    
    difference = fuzzy_combined - traditional_score
    print(f"\n   📈 Difference: {difference:+.3f} ({difference*100:+.1f}%)")
    
    if difference > 0:
        print(f"   ✅ Fuzzy logic ranks this product HIGHER (better handling of uncertainty)")
    elif difference < 0:
        print(f"   ⚠️ Fuzzy logic ranks this product LOWER (stricter linguistic rules)")
    else:
        print(f"   ➖ Both methods give same score")

def main():
    print("\n🧪 FUZZY LOGIC SYSTEM TEST SUITE")
    print("Testing Mamdani Fuzzy Inference Implementation")
    print("Based on: Zadeh (1965), Mamdani & Assilian (1975)\n")
    
    try:
        test_membership_functions()
        test_fuzzification()
        test_fuzzy_inference()
        test_comparison()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print("\n📖 See full documentation in: .methods/fuzzy_logic_system.md")
        print("🔬 Implementation: backend/home/custom_recommendation_engine.py")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
