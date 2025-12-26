class ScoringService:
    """신용 점수 계산 서비스"""
    
    def calculate_score(self, data):
        """신용 점수 계산"""
        total_score = 0
        
        # 소득 점수 (최대 300점)
        income = data.get('income', 0)
        income_score = self._calculate_income_score(income)
        total_score += income_score
        
        # 신용 이력 점수 (최대 300점)
        credit_history = data.get('credit_history', 0)
        credit_score = self._calculate_credit_history_score(credit_history)
        total_score += credit_score
        
        # 부채 비율 점수 (최대 200점)
        debt_ratio = data.get('debt_ratio', 0)
        debt_score = self._calculate_debt_ratio_score(debt_ratio)
        total_score += debt_score
        
        # 고용 안정성 점수 (최대 200점)
        employment_years = data.get('employment_years', 0)
        employment_score = self._calculate_employment_score(employment_years)
        total_score += employment_score
        
        return min(total_score, 1000)  # 최대 1000점
    
    def _calculate_income_score(self, income):
        """소득 점수 계산"""
        if income >= 10000:
            return 300
        elif income >= 7000:
            return 250
        elif income >= 5000:
            return 200
        elif income >= 3000:
            return 150
        elif income >= 2000:
            return 100
        else:
            return 50
    
    def _calculate_credit_history_score(self, months):
        """신용 이력 점수 계산"""
        if months >= 120:  # 10년 이상
            return 300
        elif months >= 60:  # 5년 이상
            return 250
        elif months >= 36:  # 3년 이상
            return 200
        elif months >= 24:  # 2년 이상
            return 150
        elif months >= 12:  # 1년 이상
            return 100
        else:
            return 50
    
    def _calculate_debt_ratio_score(self, ratio):
        """부채 비율 점수 계산"""
        if ratio <= 0.2:
            return 200
        elif ratio <= 0.4:
            return 150
        elif ratio <= 0.6:
            return 100
        elif ratio <= 0.8:
            return 50
        else:
            return 0
    
    def _calculate_employment_score(self, years):
        """고용 안정성 점수 계산"""
        if years >= 10:
            return 200
        elif years >= 5:
            return 150
        elif years >= 3:
            return 100
        elif years >= 1:
            return 50
        else:
            return 20
    
    def get_credit_grade(self, score):
        """신용 등급 산출"""
        if score >= 900:
            return '1등급'
        elif score >= 800:
            return '2등급'
        elif score >= 700:
            return '3등급'
        elif score >= 600:
            return '4등급'
        elif score >= 500:
            return '5등급'
        elif score >= 400:
            return '6등급'
        elif score >= 300:
            return '7등급'
        elif score >= 200:
            return '8등급'
        elif score >= 100:
            return '9등급'
        else:
            return '10등급'
