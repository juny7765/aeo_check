import os
import argparse
from datetime import datetime

# 김부장 스타일 마케팅 에이전트 '김대리'
# v1.0: 기본 제안서 작성 기능

def generate_proposal(project_name, target_audience, key_benefit):
    """
    마케팅 제안타를 생성하는 핵심 함수입니다.
    현재는 템플릿 기반으로 작동하며, 추후 LLM 연동 예정입니다.
    """
    
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    # 제안서 템플릿 (Markdown)
    proposal_content = f"""# [{project_name}] 마케팅 제안서

**작성일:** {timestamp}
**작성자:** 마케팅 천재 김대리 (AI Agent)

---

## 1. 프로젝트 개요
- **상품명:** {project_name}
- **핵심 강점 (USP):** {key_benefit}
- **타겟 고객:** {target_audience}

## 2. 타겟 페르소나 분석
> "{target_audience}" 그들은 누구인가?

- **니즈(Needs):** {key_benefit}을(를) 통해 현재의 문제를 해결하고 싶어함.
- **고통(Pain Point):** 기존 솔루션의 비효율성.
- **행동 패턴:** 효율성을 중시하며, 검증된 솔루션에 지갑을 엶.

## 3. 핵심 마케팅 전략 (The Strategy)

### 전략 1: "메시지 초개인화"
- 메인 카피: "당신의 비즈니스, {key_benefit}으로 완벽하게 진화합니다."
- 서브 카피: "{project_name}, 지금이 가장 빠른 도입 타이밍입니다."

### 전략 2: "채널 믹스 (Channel Mix)"
1. **링크드인/브런치:** 전문가 타겟 심층 아티클 발행.
2. **유튜브 숏츠:** {key_benefit}의 즉각적 효과 시연 영상 (15초).
3. **이메일 뉴스레터:** 기존 잠재 고객 대상 콜드 메일 발송.

## 4. 실행 타임라인 (Action Plan)
- **1주차:** 타겟 고객 데이터 수집 및 콘텐츠 기획
- **2주차:** 채널별 콘텐츠 제작 및 테스트 광고 집행
- **3주차:** 성과 분석 및 예산 최적화 (Scaling)

---
"대표님, 이 제안서대로만 진행하시면 매출 3배 상승은 시간문제입니다! - 김대리 드림"
"""
    return proposal_content

def save_proposal(content, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ 제안서 저장 완료: {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="마케팅 제안서 자동 생성 에이전트")
    parser.add_argument("--name", required=True, help="프로젝트 또는 상품 이름")
    parser.add_argument("--target", required=True, help="타겟 고객층")
    parser.add_argument("--benefit", required=True, help="핵심 강점 (USP)")
    
    args = parser.parse_args()
    
    print(f"😎 김대리가 '{args.name}' 마케팅 제안서를 고민 중입니다...")
    
    proposal = generate_proposal(args.name, args.target, args.benefit)
    
    filename = f"{args.name.replace(' ', '_')}_제안서.md"
    save_proposal(proposal, filename)
    print("🚀 작업 끝! 퇴근하겠습니다! (농담입니다)")
