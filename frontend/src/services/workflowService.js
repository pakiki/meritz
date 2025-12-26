export const nodeTypes = {
  START: 'start',
  END: 'end',
  DECISION: 'decision',
  SCORE: 'score',
  API: 'api',
};

export const nodeTypeLabels = {
  [nodeTypes.START]: '시작',
  [nodeTypes.END]: '종료',
  [nodeTypes.DECISION]: '의사결정',
  [nodeTypes.SCORE]: '점수 계산',
  [nodeTypes.API]: 'API 호출',
};

export const validateWorkflowStructure = (nodes, edges) => {
  const errors = [];
  const warnings = [];

  // 시작 노드 확인
  const startNodes = nodes.filter((node) => node.type === nodeTypes.START);
  if (startNodes.length === 0) {
    errors.push('시작 노드가 없습니다.');
  } else if (startNodes.length > 1) {
    errors.push('시작 노드가 여러 개 있습니다.');
  }

  // 종료 노드 확인
  const endNodes = nodes.filter((node) => node.type === nodeTypes.END);
  if (endNodes.length === 0) {
    warnings.push('종료 노드가 없습니다.');
  }

  // 연결되지 않은 노드 확인
  const connectedNodeIds = new Set();
  edges.forEach((edge) => {
    connectedNodeIds.add(edge.source);
    connectedNodeIds.add(edge.target);
  });

  const isolatedNodes = nodes.filter(
    (node) =>
      !connectedNodeIds.has(node.id) && node.type !== nodeTypes.START
  );

  if (isolatedNodes.length > 0) {
    warnings.push(
      `연결되지 않은 노드가 ${isolatedNodes.length}개 있습니다.`
    );
  }

  return {
    valid: errors.length === 0,
    errors,
    warnings,
  };
};

export const convertToApiFormat = (nodes, edges) => {
  return {
    nodes: nodes.map((node) => ({
      node_id: node.id,
      node_type: node.type,
      label: node.data.label,
      position: {
        x: node.position.x,
        y: node.position.y,
      },
      config: node.data.config || {},
    })),
    edges: edges.map((edge) => ({
      edge_id: edge.id,
      source: edge.source,
      target: edge.target,
      sourceHandle: edge.sourceHandle,
      targetHandle: edge.targetHandle,
      label: edge.label,
      condition: edge.data?.condition,
    })),
  };
};

export const convertFromApiFormat = (workflow) => {
  return {
    nodes: workflow.nodes.map((node) => ({
      id: node.node_id,
      type: node.node_type,
      position: node.position,
      data: {
        label: node.label,
        config: node.config,
      },
    })),
    edges: workflow.edges.map((edge) => ({
      id: edge.edge_id,
      source: edge.source,
      target: edge.target,
      sourceHandle: edge.sourceHandle,
      targetHandle: edge.targetHandle,
      label: edge.label,
      data: {
        condition: edge.condition,
      },
    })),
  };
};
