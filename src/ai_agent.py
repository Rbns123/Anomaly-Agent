# ============================================================
# AI BUSINESS ANOMALY AGENT
# Free Local Explanation Engine
# ============================================================


def generate_explanation(
    date,
    changes,
    root_cause,
    confidence
):
    """
    Generate a business-friendly explanation
    using anomaly evidence and root cause.
    """

    # Get metric changes safely
    visitors = changes.get("visitors", 0)
    conversion = changes.get("conversion_rate", 0)
    orders = changes.get("orders", 0)
    revenue = changes.get("revenue", 0)
    refunds = changes.get("refunds", 0)
    marketing = changes.get("marketing_spend", 0)

    # --------------------------------------------------------
    # CHECKOUT / PAYMENT PROBLEM
    # --------------------------------------------------------

    if root_cause == "checkout_problem":

        summary = (
            f"On {date}, website traffic remained relatively stable, "
            f"but conversion rate changed by {conversion:.2f}% and "
            f"orders changed by {orders:.2f}%. "
            f"At the same time, refunds increased by {refunds:.2f}%. "
            f"This combination strongly suggests a checkout or "
            f"payment-related problem."
        )

        recommendations = [
            "Immediately check checkout and payment gateway logs.",
            "Test the complete purchase journey from cart to payment.",
            "Verify whether the payment provider reported errors or outages.",
            "Check failed-payment and abandoned-cart rates.",
            "Compare the incident with previous successful checkout periods."
        ]

    # --------------------------------------------------------
    # CONVERSION PROBLEM
    # --------------------------------------------------------

    elif root_cause == "conversion_problem":

        summary = (
            f"On {date}, website traffic changed by {visitors:.2f}%, "
            f"while the conversion rate changed by {conversion:.2f}%. "
            f"This indicates that visitors were still reaching the "
            f"website, but a smaller percentage completed a purchase."
        )

        recommendations = [
            "Check website landing pages and product pages.",
            "Review the checkout funnel for drop-off points.",
            "Check whether recent website changes affected conversion.",
            "Compare conversion rates across devices and browsers.",
            "Investigate customer complaints during this period."
        ]

    # --------------------------------------------------------
    # REFUND PROBLEM
    # --------------------------------------------------------

    elif root_cause == "refund_problem":

        summary = (
            f"On {date}, refunds increased by {refunds:.2f}% compared "
            f"with the normal baseline. This indicates an unusual "
            f"increase in customers requesting refunds or transactions "
            f"being reversed."
        )

        recommendations = [
            "Review the most common refund reasons.",
            "Check whether a specific product has unusually high refunds.",
            "Investigate payment reversals and duplicate transactions.",
            "Review customer complaints during the anomaly period.",
            "Compare refund rates across products and regions."
        ]

    # --------------------------------------------------------
    # REVENUE PROBLEM
    # --------------------------------------------------------

    elif root_cause == "revenue_problem":

        summary = (
            f"On {date}, revenue changed by {revenue:.2f}% compared "
            f"with the normal baseline. The decline represents a "
            f"significant business impact and should be investigated "
            f"alongside orders, conversion rate, and traffic."
        )

        recommendations = [
            "Check whether the revenue decline came from fewer orders.",
            "Compare average order value with the normal baseline.",
            "Review conversion rate and website traffic.",
            "Check product availability and pricing changes.",
            "Investigate marketing campaigns and sales channels."
        ]

    # --------------------------------------------------------
    # MARKETING PROBLEM
    # --------------------------------------------------------

    elif root_cause == "marketing_problem":

        summary = (
            f"On {date}, marketing spending increased by "
            f"{marketing:.2f}% while revenue changed by "
            f"{revenue:.2f}%. This suggests that additional marketing "
            f"spending did not produce the expected business return."
        )

        recommendations = [
            "Review campaign performance and return on ad spend.",
            "Identify campaigns with unusually high spending.",
            "Compare traffic quality from each marketing channel.",
            "Pause or optimize campaigns with poor conversion.",
            "Check whether the anomaly is isolated to one channel."
        ]

    # --------------------------------------------------------
    # GENERAL BUSINESS ANOMALY
    # --------------------------------------------------------

    else:

        summary = (
            f"On {date}, multiple business metrics deviated from "
            f"their normal baseline. The detected pattern does not "
            f"match one specific failure category, so several "
            f"business factors should be investigated."
        )

        recommendations = [
            "Compare all affected metrics with the previous normal period.",
            "Check recent business, product, or technical changes.",
            "Review customer and operational activity around the anomaly.",
            "Investigate whether the anomaly is isolated or recurring.",
            "Monitor the same metrics over the next few periods."
        ]

    # --------------------------------------------------------
    # BUSINESS IMPACT
    # --------------------------------------------------------

    if revenue < -50:
        impact = (
            f"Revenue decreased by {abs(revenue):.2f}%, "
            f"indicating a very significant financial impact."
        )

    elif revenue < -20:
        impact = (
            f"Revenue decreased by {abs(revenue):.2f}%, "
            f"indicating a significant financial impact."
        )

    elif revenue < 0:
        impact = (
            f"Revenue decreased by {abs(revenue):.2f}%, "
            f"indicating a moderate financial impact."
        )

    else:
        impact = (
            "The detected anomaly did not produce a major "
            "negative revenue movement."
        )

    # --------------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------------

    result = {
        "anomaly_summary": summary,
        "confidence": confidence,
        "business_impact": impact,
        "recommended_actions": recommendations
    }

    return result


# ============================================================
# TEST THE AGENT
# ============================================================

if __name__ == "__main__":

    test_changes = {
        "visitors": -2.57,
        "conversion_rate": -69.97,
        "orders": -69.28,
        "revenue": -64.08,
        "refunds": 399.49,
        "marketing_spend": -16.97
    }

    result = generate_explanation(
        date="2025-10-25",
        changes=test_changes,
        root_cause="checkout_problem",
        confidence="VERY HIGH"
    )

    print("\n" + "=" * 60)
    print("🤖 AI BUSINESS ANOMALY AGENT")
    print("=" * 60)

    print("\nANOMALY SUMMARY:")
    print(result["anomaly_summary"])

    print("\nCONFIDENCE:")
    print(result["confidence"])

    print("\nBUSINESS IMPACT:")
    print(result["business_impact"])

    print("\nRECOMMENDED ACTIONS:")

    for number, action in enumerate(
        result["recommended_actions"],
        start=1
    ):
        print(f"{number}. {action}")

    print("\n" + "=" * 60)
    print("AI ANALYSIS COMPLETE")
    print("=" * 60)