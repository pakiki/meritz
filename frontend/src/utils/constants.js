// 애플리케이션 상수

export const APPLICATION_STATUS = {
  PENDING: 'pending',
  PROCESSING: 'processing',
  COMPLETED: 'completed',
  REJECTED: 'rejected',
  ERROR: 'error',
};

export const APPLICATION_STATUS_LABELS = {
  [APPLICATION_STATUS.PENDING]: '대기 중',
  [APPLICATION_STATUS.PROCESSING]: '처리 중',
  [APPLICATION_STATUS.COMPLETED]: '완료',
  [APPLICATION_STATUS.REJECTED]: '거절됨',
  [APPLICATION_STATUS.ERROR]: '오류',
};

export const WORKFLOW_STATUS = {
  DRAFT: 'draft',
  ACTIVE: 'active',
  ARCHIVED: 'archived',
};

export const WORKFLOW_STATUS_LABELS = {
  [WORKFLOW_STATUS.DRAFT]: '초안',
  [WORKFLOW_STATUS.ACTIVE]: '활성',
  [WORKFLOW_STATUS.ARCHIVED]: '보관됨',
};

export const NODE_TYPES = {
  START: 'start',
  END: 'end',
  DECISION: 'decision',
  SCORE: 'score',
  API: 'api',
};

export const RULE_TYPES = {
  SCORE: 'score',
  DECISION: 'decision',
  VALIDATION: 'validation',
};

export const CREDIT_GRADES = [
  '1등급',
  '2등급',
  '3등급',
  '4등급',
  '5등급',
  '6등급',
  '7등급',
  '8등급',
  '9등급',
  '10등급',
];

export const API_ENDPOINTS = {
  WORKFLOW: '/workflow',
  APPLICATION: '/application',
  ENGINE: '/engine',
};
